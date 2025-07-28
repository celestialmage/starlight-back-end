from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
import datetime
from datetime import datetime as time
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING
from .like import Like
from .user import User

if TYPE_CHECKING:
    from .reply import Reply

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'), index=True)
    text: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    user: Mapped['User'] = relationship(back_populates='posts')
    time_posted: Mapped[datetime.datetime] = mapped_column(DateTime())
    liked_by: Mapped[list['User']] = relationship(secondary=Like.__table__, back_populates='likes')
    replies: Mapped[list['Reply']] = relationship(back_populates='post')

    def get_replies(self):
        return self.replies

    def get_liked_by(self):
        return self.liked_by

    def liked_count(self):
        return len(self.liked_by)

    def to_dict(self, user=False):
        post = {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'image': self.image,
            'time_posted': self.time_posted,
            'reply_count': len(self.replies),
            'like_count': len(self.liked_by)
        }

        if user:
            post['user'] = self.user.to_dict()

        return post

    @classmethod
    def from_dict(cls, post_data):
        new_post = Post(
            user_id=post_data['user_id'],
            text=post_data['text'],
            time_posted=time.now()
        )

        return new_post