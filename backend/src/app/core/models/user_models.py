from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"  

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username : Mapped[str] = mapped_column(String, unique=True, index=True)
    password : Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    token : Mapped[str] = mapped_column(String, unique=True)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
