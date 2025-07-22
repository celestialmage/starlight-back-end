from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
import datetime
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True)
    text: Mapped[Optional[str]]
    image: Mapped[Optional[str]]
    time_posted: Mapped[DateTime]
    likes: Mapped[list['Like']] = relationship(back_populates='post')