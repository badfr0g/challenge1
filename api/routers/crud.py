from fastapi import APIRouter, HTTPException, status
from api.models.crud import Comment, CommentHistory
from api.schemas.crud import GetComment, PostComment, PutComment, GetCommentHistory, UpdateCommentHistory
from datetime import datetime

crud_router = APIRouter(prefix="/api", tags=["CRUD Operations"])

@crud_router.get("/")
async def crud_get():
    data = Comment.all()
    return await GetComment.from_queryset(data)

@crud_router.post("/")
async def crud_post(comment: PostComment):
    row = await Comment.create(**comment.model_dump(exclude_unset=True))
    return await GetComment.from_tortoise_orm(row)

@crud_router.put("/{key}")
async def crud_put(key: int, comment: PutComment):
    data = comment.model_dump(exclude_unset=True)
    dataBeforeUpdate = await GetComment.from_queryset(Comment.filter(id=key))
    exists = await Comment.filter(id=key).exists()
    history_exists = await CommentHistory.filter(comment_id=key).exists()  
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    if not history_exists:
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
    await Comment.filter(id=key).update(**data)
    return await GetComment.from_queryset_single(Comment.get(id=key))

@crud_router.delete("/{key}")
async def crud_delete(key: int):
    exists = await Comment.filter(id=key).exists()
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    await Comment.filter(id=key).delete()
    return "Comment deleted successfully"

@crud_router.get("/commentHistory")
async def crud_get():
    print("in history")
    data = CommentHistory.all()
    return await GetCommentHistory.from_queryset(data)
