import pytest
from pydantic import ValidationError


from dbbackup.connection import ConnectionParams , DatabaseType


def test_network_db_gets_fedault_host_and_port():
    params = ConnectionParams(db_type=DatabaseType.POSTGRESQL,database="app")
    assert params.host == "localhost"
    assert params.port == 5432


def test_explicit_values_are_kept():
    params = ConnectionParams(
        db_type=DatabaseType.MYSQL , database="app",host="db.internal",port=3307
            )
    assert params.host == "db.internal"
    assert params.port == 3307


def test_sqlite_rejects_network_fields():
    with pytest.raises(ValidationError):
        ConnectionParams(db_type=DatabaseType.SQLITE,database="x.db",host="h")

def test_port_out_of_range_is_rejected():
    with pytest.raises(ValidationError):
        ConnectionParams(db_type=DatabaseType.MYSQL,database="app",port=70000)

def test_password_is_never_shown_in_repr_or_str():
    params = ConnectionParams(
        db_type = DatabaseType.POSTGRESQL, database="app", password = "s3cret"
        )
    assert "s3cret" not in repr(params)
    assert "s3cret" not in str(params)
    assert params.password.get_secret_value() == "s3cret"
