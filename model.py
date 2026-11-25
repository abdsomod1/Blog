from db import db
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey

class Category (db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    posts: Mapped [list[Post]] = relationship(back_populates='category_')

class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=lambda:datetime.now(timezone.utc))
    cat_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    
    category_: Mapped[Category] = relationship(back_populates='posts')



