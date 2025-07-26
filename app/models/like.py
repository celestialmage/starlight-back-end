from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id
        }
    
    @classmethod
    def from_dict(cls, like_data):
        new_like = Like(
            post_id=like_data['post_id'],
            user_id=like_data['user_id']
        )

        return new_like


    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )