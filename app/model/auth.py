from datetime import datetime
import enum

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    String,
)

from .base import BaseModel


class UserPermission(enum.Enum):
    ANONYMOUS = "ANONYMOUS"  # 비회원
    NORMAL = "NORMAL"  # 일반 회원
    ADMIN = "ADMIN"  # 관리자
    MASTER = "MASTER"  # 마스터

    def is_authenticated(self):
        return self in (self.NORMAL, self.ADMIN, self.MASTER)


class AuthUser(BaseModel):
    __tablename__ = "tb_auth_user"

    id = Column(BigInteger, primary_key=True)
    email = Column(String(200), comment="사용자 이메일", nullable=False, unique=True)
    password = Column(String(128), comment="비밀번호", nullable=True)
    permission = Column(
        Enum(UserPermission, native_enum=False, length=20),
        comment="주문 상태",
        nullable=False,
        default=UserPermission.NORMAL,
    )
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    last_login = Column(
        DateTime(timezone=True), comment="주문 확정 일시", nullable=True
    )
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
