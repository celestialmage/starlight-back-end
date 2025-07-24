from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger
from typing import Optional
from ..db import db
from typing import TYPE_CHECKING
from .like import Like
from .follow import Follow


if TYPE_CHECKING:
    from .post import Post

class User(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, index=True, unique=True)
    username: Mapped[str]
    bio: Mapped[str]
    display_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)

    posts: Mapped[list['Post']] = relationship(back_populates='user')
    likes: Mapped[list['Post']] = relationship(secondary=Like.__table__, back_populates='liked_by')
    
    following_associations: Mapped[list['Follow']] = relationship(
        'Follow',
        foreign_keys='[Follow.follower_id]',
        back_populates='follower',
        cascade='all, delete-orphan'
    )

    follower_associations: Mapped[list['Follow']] = relationship(
        'Follow',
        foreign_keys='[Follow.followed_id]',
        back_populates='followed',
        cascade='all, delete-orphan'
    )

    following: Mapped[list['User']] = relationship(
        'User',
        secondary=Follow.__table__,
        primaryjoin='User.id==Follow.follower_id',
        secondaryjoin='User.id==Follow.followed_id',
        backref='followers',
        viewonly=True
    )

    def to_dict(self):

        return {
            'id': self.id,
            'username': self.username,
            'bio': self.bio,
            'display_name': self.display_name,
            'email': self.email
        }
    
    def get_posts(self):
        return self.posts
    
    def get_likes(self):
        return self.likes
    
    def get_following(self):
        return self.following
    
    def get_followers(self):
        return self.followers
    
    @classmethod
    def from_dict(cls, user_data):

        print(user_data)

        new_user = User(
            username=user_data['username'],
            display_name=user_data['display_name'],
            bio=user_data['bio'],
            email=user_data['email'],
            id=user_data['id']
        )

        return new_user