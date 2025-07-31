from fastapi import APIRouter, HTTPException, status, Depends
from api.models.crud import Comment, CommentHistory, User
from api.schemas.crud import GetComment, PostComment, PutComment, GetCommentHistory
from authentication.auth import authenticate_user, create_access_token, get_current_user
from datetime import datetime, timedelta
from pydantic import BaseModel
from passlib.hash import bcrypt


class SignUpRequest(BaseModel):
    username: str
    password: str
    user_group: str

class LoginRequest(BaseModel):
    username: str
    password: str

crud_router = APIRouter(tags=["CRUD Operations"])

@crud_router.get("/")
async def crud_get(current_user: User = Depends(get_current_user)):
    data = Comment.all()
    return await GetComment.from_queryset(data)

@crud_router.post("/")
async def crud_post(comment: PostComment, current_user: User = Depends(get_current_user)):
    row = await Comment.create(
        user=current_user.username,
        content=comment.content
    )
    return await GetComment.from_tortoise_orm(row)

@crud_router.put("/{key}")
async def crud_put(key: int, comment: PutComment, current_user: User = Depends(get_current_user)):
    dataBeforeUpdate = await GetComment.from_queryset(Comment.filter(id=key))
    if comment.user != dataBeforeUpdate[0].user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permission denied: You are not the creator of the comment "
        )
    else:
        isCommentExists = await Comment.filter(id=key).exists()
        isCommentHistoryExists = await CommentHistory.filter(comment_id=key).exists()  
        if not isCommentExists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment Not Found"
            )
        if not isCommentHistoryExists:
            db_comment = await Comment.get(id=key)
            await CommentHistory.create(
                last_update_time=datetime.utcnow(),
                old_value=dataBeforeUpdate[0].content,
                new_value=comment.content,
                comment=db_comment
            )
        else:
            await CommentHistory.filter(comment_id=key).update(
                last_update_time=datetime.utcnow(),
                old_value=dataBeforeUpdate[0].content,
                new_value=comment.content
            )  
        await Comment.filter(id=key).update(
            content=comment.content
        )
        return await GetComment.from_queryset_single(Comment.get(id=key))

@crud_router.delete("/{key}")
async def crud_delete(key: int):
    isCommentExists = await Comment.filter(id=key).exists()
    if not isCommentExists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    await Comment.filter(id=key).delete()
    return "Comment deleted successfully"

@crud_router.get("/commentHistory")
async def crud_get(current_user: User = Depends(get_current_user)):
    print("in history")
    data = CommentHistory.all()
    return await GetCommentHistory.from_queryset(data)

@crud_router.post("/signup")
async def signup(request: SignUpRequest):
    existing = await User.get_or_none(username=request.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = await User.create(username=request.username, hashed_password=bcrypt.hash(request.password), user_group=request.user_group)
    return {"message": "User created"}

@crud_router.post("/login")
async def login(request: LoginRequest):
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}