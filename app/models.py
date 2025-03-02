from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column, INTEGER, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(INTEGER, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id = Column(INTEGER, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "Users"

    id = Column(INTEGER, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    