from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Follow(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    followed_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

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


    __table_args__ = (
        UniqueConstraint("follower_id", "followed_id", name="unique_follower_followed")
    )