from pydantic import BaseModel, Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.crud import Comment, CommentHistory

GetComment = pydantic_model_creator(Comment, name="comment")
GetCommentHistory = pydantic_model_creator(CommentHistory, name="comment_history")

class PostComment(BaseModel):
    content: str = Field(..., description="Content of the comment") 

class PutComment(BaseModel):
    content: Optional[str] = Field(None, description="Content of the comment")