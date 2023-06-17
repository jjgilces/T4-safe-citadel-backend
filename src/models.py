from config.database import Base
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum
from auth import AuthHandler

auth_handler = AuthHandler()


class VisitState(Enum):
    PENDING = "PENDING"
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True, unique=True, default=None)
    is_active = Column(Boolean, default=True)
    resident = relationship(
        "Resident",
        back_populates="user",
    )
    guard = relationship(
        "Guard",
        back_populates="user",
    )

    def __str__(self):
        return self.username

    def verify_password(self, password):
        auth_handler.verify_password(password, self.password)


class Visit(Base):
    __tablename__ = "visit"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.now)
    date = Column(DateTime, nullable=False)
    state = Column(ENUM(VisitState), nullable=False, default=VisitState.PENDING)
    additional_info = Column(JSON, nullable=True)
    qr_id = Column(UUID(as_uuid=True), ForeignKey("qr.id"))
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitor.id"))
    guard_id = Column(UUID(as_uuid=True), ForeignKey("guard.id"))
    resident_id = Column(UUID(as_uuid=True), ForeignKey("resident.id"))
    qr = relationship("Qr", foreign_keys=[qr_id])
    visitor = relationship("Visitor", foreign_keys=[visitor_id])
    guard = relationship("Guard", foreign_keys=[guard_id])
    resident = relationship("Resident", foreign_keys=[resident_id])


class Visitor(Base):
    __tablename__ = "visitor"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.name


class FrequentVisitor(Base):
    __tablename__ = "frequent_visitor"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), ForeignKey("resident.id"), primary_key=True)
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitor.id"))


class Residence(Base):
    __tablename__ = "residence"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    address = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    information = Column(JSON, nullable=True)

    def __str__(self):
        return self.address


class Guard(Base):
    __tablename__ = "guard"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id], back_populates="guard")

    def __str__(self):
        return f"{self.user.username}"


class Resident(Base):
    __tablename__ = "resident"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    phone = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id], back_populates="resident")
    residence_id = Column(UUID(as_uuid=True), ForeignKey("residence.id"))
    residence = relationship("Residence", foreign_keys=[residence_id], cascade="delete")

    def __str__(self):
        return f"{self.user}"


class Qr(Base):
    __tablename__ = "qr"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.now)
    code = Column(String, default=str(uuid4()))

    def __str__(self):
        return self.code
