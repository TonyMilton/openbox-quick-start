from sqlalchemy import String, Integer, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


class WeatherRecord(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    location: Mapped[str] = mapped_column(String(100))
    weather_status: Mapped[str] = mapped_column(String(100))
    temperature: Mapped[float] = mapped_column(Float)
    humidity: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"<WeatherRecord(id={self.id}, location={self.location}, temperature={self.temperature}, timestamp={self.timestamp})>"
