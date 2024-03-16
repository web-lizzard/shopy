from datetime import timezone

from sqlalchemy import Column, String, func
from sqlalchemy.types import DateTime, TypeDecorator
import uuid

class TimezoneAwareDateTime(TypeDecorator):
    """Results returned as aware datetimes, not naive ones."""

    impl = DateTime

    def process_result_value(self, value, dialect):
        if value:
            return value.replace(tzinfo=timezone.utc)
        return value


class IdentifierMixin:
    id = Column(String(60), index=True, unique=True, default= lambda : str(uuid.uuid4()), primary_key=True)


class TimestampMixin:
    created_at = Column(TimezoneAwareDateTime, default=func.now())
    modified_at = Column(TimezoneAwareDateTime, default=func.now())
    deleted_at = Column(TimezoneAwareDateTime)
