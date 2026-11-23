from enum import StrEnum
from typing import Self

from pydantic import BaseModel, Field, SecretStr, model_validator


class DatabaseType(StrEnum):
    """Supported database management systems."""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"


DEFAULT_PORTS: dict[DatabaseType, int] = {
    DatabaseType.POSTGRESQL: 5432,
    DatabaseType.MYSQL: 3306,
    DatabaseType.MONGODB: 27017,
}


class ConnectionParams(BaseModel):
    """Everything needed to connect to a database."""

    db_type: DatabaseType
    database: str = Field(min_length=1)
    host: str | None = None
    port: int | None = Field(default=None, ge=1, le=65535)
    username: str | None = None
    password: SecretStr | None = None

    @model_validator(mode="after")
    def _check_and_fill_defaults(self) -> Self:
        if self.db_type is DatabaseType.SQLITE:
            unused = {
                "host": self.host,
                "port": self.port,
                "username": self.username,
                "password": self.password,
            }
            given = [name for name, value in unused.items() if value is not None]
            if given:
                raise ValueError(
                    f"{', '.join(given)} not supported for sqlite "
                    "(it is a local file; use only --database as the file path)"
                )
            return self

        if self.host is None:
            self.host = "localhost"
        if self.port is None:
            self.port = DEFAULT_PORTS[self.db_type]
        return self
