from sqlalchemy import String, ForeignKey, Float, Integer, Table, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
from db.database import Base
from typing import Optional

# Таблица для связи многие ко многим между Organization и Activity
organization_activity = Table(
    "organization_activity", Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activitys.id"), primary_key=True)
)

class Building(Base):
    address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations: Mapped["Organization"] = relationship("Organization", back_populates="building")

class Activity(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("activitys.id"), nullable=True)

    parent: Mapped["Activity"] = relationship("Activity", remote_side=[id], back_populates="children")
    children: Mapped[list["Activity"]] = relationship("Activity", back_populates="parent")
    organizations: Mapped[list["Organization"]] = relationship("Organization", secondary=organization_activity, back_populates="activities")

class Organization(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone_numbers: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building: Mapped["Building"] = relationship("Building", back_populates="organizations")
    activities: Mapped[list["Activity"]] = relationship("Activity", secondary=organization_activity, back_populates="organizations")
