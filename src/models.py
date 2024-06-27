import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    bio = Column(String(150), nullable=True)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)

    # Relación con Story (user es el padre)
    stories = relationship("Story", back_populates="user")

    # Relación con Post (user es el padre)
    posts = relationship("Post", back_populates="user")

class Story(Base):
    __tablename__ = "story"
    id = Column(Integer, primary_key=True)
    image_url = Column(String(520), nullable=False)
    time = Column(DateTime, nullable=False)
    auto_delete_24hs = Column(DateTime, nullable=False)

    # Relación con Story (story es el hijo)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates = "stories")
    
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    image_url = Column(String(520), nullable=False)
    bio = Column(String(100), nullable=True)
    time = Column(DateTime, nullable=False)

    # Relación con Post (post es el hijo)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates = "posts")

    # Relación con like, saved y comment (post es el padre)
    likes = relationship("Like", back_populates="post")
    saved_posts = relationship("Saved", back_populates="post")
    comments = relationship("Comment", back_populates="post")


class Like(Base):
    __tablename__ = "like"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    # Relación con post (like es el hijo)
    post = relationship("Post", back_populates = "likes")
    
class Saved(Base):
    __tablename__ = "saved"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    # Relación con post (saved es el hijo)
    post = relationship("Post", back_populates = "saved_posts")

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    text = Column(String(120), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    # Relación con post (comment es el hijo)
    post = relationship("Post", back_populates = "comments")



## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e

