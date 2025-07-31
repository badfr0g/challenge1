from tortoise.models import Model
from tortoise.fields import CharField, IntField,  DatetimeField   , TextField, ForeignKeyField, CASCADE
from datetime import datetime
from passlib.hash import bcrypt

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

class User(Model):
    id = IntField(pk=True)
    username = CharField(max_length=50, unique=True)
    hashed_password = CharField(max_length=128)
    user_group = CharField(max_length=128)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)