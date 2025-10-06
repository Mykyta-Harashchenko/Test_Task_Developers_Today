import enum
from sqlalchemy import Integer, String, Float, Boolean, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base

Base = declarative_base()

class SpyCat(Base):
    __tablename__ = "spy_cats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    years_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(50), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    missions: Mapped[list["Mission"]] = relationship("Mission", back_populates="cat")

class Mission(Base):
    __tablename__ = "missions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cat_id: Mapped[int] = mapped_column(Integer, ForeignKey("spy_cats.id"), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    cat: Mapped["SpyCat"] = relationship("SpyCat", back_populates="missions")
    targets: Mapped[list["Target"]] = relationship("Target", back_populates="mission", cascade="all, delete-orphan")

class Target(Base):
    __tablename__ = "targets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mission_id: Mapped[int] = mapped_column(Integer, ForeignKey("missions.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    mission: Mapped["Mission"] = relationship("Mission", back_populates="targets")