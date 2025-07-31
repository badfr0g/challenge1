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

# Get all comment
@crud_router.get("/")
async def crud_get(current_user: User = Depends(get_current_user)):
    user_group = current_user.user_group
    user_in_group = await User.filter(user_group=user_group).values_list("username", flat=True)
    data = Comment.filter(user__in=user_in_group)
    return await GetComment.from_queryset(data)
 
# Create new record
@crud_router.post("/")
async def crud_post(comment: PostComment, current_user: User = Depends(get_current_user)):
    row = await Comment.create(
        user=current_user.username,
        content=comment.content
    )
    return await GetComment.from_tortoise_orm(row)

# Update record
@crud_router.put("/{key}")
async def crud_put(key: int, comment: PutComment, current_user: User = Depends(get_current_user)):
    dataBeforeUpdate = await GetComment.from_queryset(Comment.filter(id=key))
    if current_user.username != dataBeforeUpdate[0].user:
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

# Delete record
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

# Get all comment history
@crud_router.get("/commentHistory")
async def crud_get(current_user: User = Depends(get_current_user)):
    user_group = current_user.user_group
    user_in_group = await User.filter(user_group=user_group).values_list("username", flat=True)
    comment_data = await Comment.filter(user__in=user_in_group).values_list("id", flat=True)
    history = CommentHistory.filter(id__in=comment_data)
    return await GetCommentHistory.from_queryset(history)

# Signup 
@crud_router.post("/signup")
async def signup(request: SignUpRequest):
    existing = await User.get_or_none(username=request.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    await User.create(username=request.username, hashed_password=bcrypt.hash(request.password), user_group=request.user_group)
    return {"message": "User created"}

# Existing login 
@crud_router.post("/login")
async def login(request: LoginRequest):
    user = await authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}