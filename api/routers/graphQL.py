import strawberry
from fastapi import Request
from typing import List
from api.models.crud import Comment, CommentHistory, User
from api.schemas.graphQL import CommentType, CommentHistoryType
from api.schemas.crud import GetComment
from authentication.auth import create_access_token,get_current_user_from_request
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@strawberry.type
class UserType:
    id: int
    username: str
    user_group: str

@strawberry.type
class AuthPayload:
    access_token: str
    token_type: str = "bearer"
    
@strawberry.type
class Query:
    @strawberry.field
    async def all_comments(self, info) -> List[CommentType]:
        request: Request = info.context["request"]
        user = await get_current_user_from_request(request)
        if not user:
            raise Exception("Unauthorized")
        return await Comment.all()

    @strawberry.field
    async def all_comment_histories(self, info) -> List[CommentHistoryType]:
        request: Request = info.context["request"]
        user = await get_current_user_from_request(request)
        if not user:
            raise Exception("Unauthorized")
        return await CommentHistory.all()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_comment(self, user: str, content: str, info) -> CommentType:
        request: Request = info.context["request"]
        user = await get_current_user_from_request(request)
        if not user:
            raise Exception("Unauthorized")
        comment = await Comment.create(user=user, content=content)
        return comment

    @strawberry.mutation
    async def update_comment(self, id: int, user:str, content: str, info) -> CommentType:
        request: Request = info.context["request"]
        user = await get_current_user_from_request(request)
        if not user:
            raise Exception("Unauthorized")
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
    async def delete_comment(self, id: int, info) -> str:
        request: Request = info.context["request"]
        user = await get_current_user_from_request(request)
        if not user:
            raise Exception("Unauthorized")
        isCommentExists = await Comment.filter(id=id).exists()
        if not isCommentExists:
            raise Exception(detail="Comment not found")
        await Comment.filter(id=id).delete()
        return "Comment deleted successfully"
    
    # Existing login mutation
    @strawberry.mutation
    async def login(self, username: str, password: str) -> AuthPayload:
        user = await User.get_or_none(username=username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            raise Exception("Invalid credentials")
        token = create_access_token({"sub": user.username})
        return AuthPayload(access_token=token)

    # New: Signup mutation
    @strawberry.mutation
    async def create_user(self, username: str, password: str, user_group: str) -> UserType:
        existing = await User.get_or_none(username=username)
        if existing:
            raise Exception("Username already taken")

        hashed_pw = pwd_context.hash(password)
        user = await User.create(username=username, hashed_password=hashed_pw, user_group=user_group)
        return UserType(id=user.id, username=user.username, user_group=user_group)
schema = strawberry.Schema(query=Query, mutation=Mutation)
