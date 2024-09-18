from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Image(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    filename: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    upload_time: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    short_link: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
    deletion_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    def __repr__(self):
        return 'Image {}'.format(self.filename)