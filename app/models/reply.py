from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
import datetime
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .post import Post

class Reply(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'), index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    text: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    time_posted: Mapped[datetime.datetime] = mapped_column(DateTime())
    post: Mapped['Post'] = relationship(back_populates='replies')

def to_dict(self):
    return {
        "id": self.id,
        "user_id": self.user_id,
        "post_id": self.post_id,
        "text": self.text,
        "image": self.image,
        "time_posted": self.time_posted
    }