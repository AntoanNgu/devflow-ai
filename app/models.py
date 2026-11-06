from sqlalchemy import String, func, ForeignKey
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass 

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    password_hash: Mapped[str]

class Repo(Base):
    __tablename__ = "repos"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    repo_url: Mapped[str] = mapped_column()
    requested_ref: Mapped[str | None]
    #snapshots_id:
    status: Mapped[str] = mapped_column(server_default="pending")
    error: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

