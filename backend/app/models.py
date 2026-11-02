from datetime import datetime

from sqlalchemy import (Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    encrypted_refresh_token: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), server_default=func.now() )

class Digest(Base):
    __tablename__ = "digests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class DigestItem(Base):
    __tablename__ = "digest_items"
    __table_args__ = (UniqueConstraint("user_id", "gmail_id"),) #Couple ("user_id", "gmail_id") must be unique. I.e. it can appear only once

    id: Mapped[int] = mapped_column(primary_key=True)
    digest_id: Mapped[int] = mapped_column(ForeignKey("digests.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    gmail_id: Mapped[str] = mapped_column(String)
    sender: Mapped[str] = mapped_column(String)
    subject: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String)
    requires_action: Mapped[bool] = mapped_column(Boolean)