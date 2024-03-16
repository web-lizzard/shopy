from datetime import timezone, datetime
import uuid

from sqlalchemy import Column, String, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, TypeDecorator

class TimezoneAwareDateTime(TypeDecorator):
    """Results returned as aware datetimes, not naive ones."""

    impl = DateTime

    def process_result_value(self, value, dialect):
        if value:
            return value.replace(tzinfo=timezone.utc)
        return value


class IdentifierMixin:
    id: Mapped[str] = mapped_column(String(60), index=True, unique=True, default= lambda : str(uuid.uuid4()), primary_key=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(TimezoneAwareDateTime, default=func.now())
    modified_at: Mapped[datetime] = mapped_column(TimezoneAwareDateTime, default=func.now())
