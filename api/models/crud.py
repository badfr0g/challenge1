from tortoise.models import Model
from tortoise.fields import CharField, IntField,  DatetimeField   , TextField, ForeignKeyField, CASCADE
from datetime import datetime


class Comment(Model):  
    id = IntField(pk=True)
    user = CharField(max_length=255)
    content = TextField()
    class Meta:
        table = "comment"


class CommentHistory(Model):
    id = IntField(pk=True)
    last_update_time = DatetimeField(default=datetime.utcnow)
    old_value = TextField()
    new_value = TextField()
    comment = ForeignKeyField(
        "models.Comment", related_name="history", on_delete=CASCADE
    )
    class Meta:
        table = "comment_history"