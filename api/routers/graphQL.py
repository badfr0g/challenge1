# schema.py
import strawberry
from typing import List
from api.models.crud import Comment, CommentHistory
from api.schemas.graphQL import CommentType, CommentHistoryType
from api.schemas.crud import GetComment, PostComment, PutComment, GetCommentHistory, UpdateCommentHistory
from datetime import datetime

@strawberry.type
class Query:
    @strawberry.field
    async def all_comments(self) -> List[CommentType]:
        print(Comment.all())
        return await Comment.all()

    @strawberry.field
    async def all_comment_histories(self) -> List[CommentHistoryType]:
        return await CommentHistory.all()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_comment(self, user: str, content: str) -> CommentType:
        comment = await Comment.create(user=user, content=content)
        return comment

    @strawberry.mutation
    async def update_comment(self, id: int, user:str, content: str) -> CommentType:
        isCommentExists = await Comment.filter(id=id).exists()       
        isCommentHistoryExists = await CommentHistory.filter(comment_id=id).exists()
        comment = await Comment.get(id=id)
        if comment.user != user:
            raise Exception("Permission denied: You are not the creator of the comment")
        else:
            if not isCommentExists:
                raise Exception("Comment Not Found")
            if not isCommentHistoryExists:
                await CommentHistory.create(
                    laslast_update_time=datetime.utcnow(),
                    old_value=comment.content,
                    comment=comment,
                    new_value=content
                )
            else:
                await CommentHistory.filter(comment_id=id).update(
                    last_update_time=datetime.utcnow(),
                    old_value=comment.content,
                    new_value=content
                )
            await Comment.filter(id=id).update(
                content=content
            )
            return await GetComment.from_queryset_single(Comment.get(id=id))

    @strawberry.mutation
    async def delete_comment(self, id: int) -> str:
        isCommentExists = await Comment.filter(id=id).exists()
        if not isCommentExists:
            raise Exception(detail="Comment not found")
        await Comment.filter(id=id).delete()
        return "Comment deleted successfully"

schema = strawberry.Schema(query=Query, mutation=Mutation)
