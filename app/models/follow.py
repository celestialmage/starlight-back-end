from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Follow(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    follower_id: Mapped[str] = mapped_column(ForeignKey('user.id'), nullable=False)
    followed_id: Mapped[str] = mapped_column(ForeignKey('user.id'), nullable=False)

    follower: Mapped['User'] = relationship(
        'User',
        foreign_keys=[follower_id],
        back_populates='following_associations'
    )
    followed: Mapped['User'] = relationship(
        'User',
        foreign_keys=[followed_id],
        back_populates="follower_associations"
    )

    def to_dict(self):
        follow = {
            "id": self.id,
            "follower_id": self.follower_id,
            "followed_id": self.followed_id
        }

        return follow

    @classmethod
    def from_dict(cls, follow_data):
        new_follow = Follow(
            follower_id=follow_data['follower_id'],
            followed_id=follow_data['followed_id']
        )

        return new_follow
    


    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="unique_follower_followed"),
    )