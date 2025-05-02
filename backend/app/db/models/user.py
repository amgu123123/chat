from typing import List

from sqlalchemy import Integer, String, TIMESTAMP
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.sql import func

from db.session import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    # email: Mapped[str] = mapped_column(String, unique=True, index=True,
    #                                    nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    username = mapped_column(String, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())
    avatar=mapped_column(String)
    messages : Mapped[List["Message"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
