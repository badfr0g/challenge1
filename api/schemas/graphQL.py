import strawberry
from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.crud import Comment, CommentHistory

Comment_Pydantic = pydantic_model_creator(Comment)
CommentHistory_Pydantic = pydantic_model_creator(CommentHistory)
CommentIn_Pydantic = pydantic_model_creator(Comment, exclude_readonly=True)
CommentHistoryIn_Pydantic = pydantic_model_creator(CommentHistory, exclude_readonly=True)

@strawberry.type
class CommentType:
    id: int
    user: str
    content: str

@strawberry.type
class CommentHistoryType:
    id: int
    old_value: str
    new_value: str
    last_update_time: str
    comment_id: int
