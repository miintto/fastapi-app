from typing import Callable, Any

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    __serialize_fields__ = ()

    @property
    def pk(self):
        return self.id

    def serialize(
        self,
        fields: list[str] = None,
        func: dict[str, Callable] = None,
    ) -> dict[str, Any]:
        if not func:
            func = {}
        return {
            col: func[col](self) if col in func else getattr(self, col)
            for col in fields or self.__serialize_fields__
        }
