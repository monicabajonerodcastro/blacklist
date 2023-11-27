from marshmallow import Schema, fields
from sqlalchemy  import  Column, String,DateTime
from src.models.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone


class BlackList(Base):
	__tablename__  =  'blacklist'
	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	email = Column(String, nullable=False)
	app_uuid = Column(String, nullable=False)
	blocked_reason = Column(String, nullable=False)
	ip = Column(String, nullable=False)
	createdAt = Column(DateTime, nullable=False)


	def  __init__(self, email, app_uuid, blocked_reason, ip_address):
		self.email = email
		self.app_uuid = app_uuid
		self.blocked_reason = blocked_reason
		self.ip=ip_address
		self.createdAt=datetime.now(timezone.utc)


class BlacklistJsonSchema(Schema):
	id = fields.UUID(dump_only=True)
	routeId  = fields.Str()
	email = fields.Str()
	app_uuid = fields.Str()
	blocked_reason  = fields.Str()
