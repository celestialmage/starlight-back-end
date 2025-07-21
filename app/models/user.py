from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post
    from .like import Like
    from .follow import Follow

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str]
    display_name: Mapped[str]
    email: Mapped[str]
    posts: Mapped[list['Post']] = relationship(back_populates='user')
    likes: Mapped[list['Like']] = relationship(back_populates='user')
    follows: Mapped[list['Follow']] = relationship(back_populates='user')

    def to_dict(self):

        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, user_data):
        return cls(
            username=user_data['username'],
            display_name=user_data['display_name'],
            email=user_data['email']
        )