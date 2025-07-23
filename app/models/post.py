from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
import datetime
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .reply import Reply

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    text: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    time_posted: Mapped[datetime.datetime] = mapped_column(DateTime())
    liked_by: Mapped[list['User']] = relationship(secondary='Like', back_populates='likes')
    replies: Mapped[list['Reply']] = relationship(back_populates='post')

def to_dict(self):
    return {
        "id": self.id,
        "user_id": self.user_id,
        "text": self.text,
        "image": self.image,
        "time_posted": self.time_posted
    }

def get_liked_by(self):
    return self.liked_by

def liked_count(self):
    return len(self.liked_by)