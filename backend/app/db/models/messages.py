from sqlalchemy import Integer, String, ForeignKey, func, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.session import Base


class Message(Base):
    __tablename__ = "messages"

    id = mapped_column(Integer, primary_key=True, index=True)
    content = mapped_column(String, nullable=False)
    created_at = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())

    user_id = mapped_column(ForeignKey("users.id"))
    user:Mapped["User"] = relationship(back_populates="messages")