from pydantic import BaseModel, Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.crud import Comment, CommentHistory
from datetime import datetime


GetComment = pydantic_model_creator(Comment, name="comment")
GetCommentHistory = pydantic_model_creator(CommentHistory, name="comment_history")

class PostComment(BaseModel):
    content: str = Field(..., description="Content of the comment") 
    user: str = Field(..., description="User who made the comment")

class PutComment(BaseModel):
    content: Optional[str] = Field(None, description="Content of the comment")
    user: Optional[str] = Field(None, description="User who made the comment")

class UpdateCommentHistory(BaseModel):
    comment_id: int = Field(..., description="ID of the comment being updated")
    last_update_time: datetime = Field(default_factory=datetime.utcnow)
    old_value: str = Field(..., description="Old value of the comment")
    new_value: str = Field(..., description="New value of the comment")