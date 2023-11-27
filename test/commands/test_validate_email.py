import pytest

from faker import Faker
from unittest.mock import patch, MagicMock

from src.models.blacklist import BlackList
from src.commands.validate_email import ValidateEmail
from src.commands.constants import Constant
from src.errors.errors import MissingRequiredToken, WrongSecretToken

fake = Faker()

def test_validate_existing_email():
    validate_email = BlackList(fake.email(), fake.uuid4(), fake.sentence(nb_words=3), fake.ipv4())

    session = MagicMock()
    query = MagicMock()

    query.filter.return_value.first.return_value = validate_email
    session.query.return_value = query

    service = ValidateEmail(session,  {"Authorization": "Bearer "+Constant.SECRET_TOKEN}, validate_email.email)

    result = service.execute()
    assert result is True

def test_validate_non_existing_email():
    session = MagicMock()
    query = MagicMock()

    query.filter.return_value.first.return_value = None
    session.query.return_value = query

    service = ValidateEmail(session,  {"Authorization": "Bearer "+Constant.SECRET_TOKEN},fake.email())

    result = service.execute()
    assert result is False

def test_validate_email_without_token():
    session = MagicMock()
    query = MagicMock()

    query.filter.return_value.first.return_value = None
    session.query.return_value = query

    with pytest.raises(MissingRequiredToken) as exc_info:
        service = ValidateEmail(session, {},fake.email())
        service.execute()

    assert not session.query.called
    assert exc_info.value.code == 403
    assert exc_info.value.description == "No existe token en la solicitud"


def test_validate_email_without_bearer_token():
    session = MagicMock()
    query = MagicMock()

    query.filter.return_value.first.return_value = None
    session.query.return_value = query

    with pytest.raises(MissingRequiredToken) as exc_info:
        service = ValidateEmail(session,  {"Authorization": "SomeToken"},fake.email())
        service.execute()

    assert not session.query.called
    assert exc_info.value.code == 403
    assert exc_info.value.description == "No existe token en la solicitud"


def test_validate_email_without_trusted_token():
    session = MagicMock()
    query = MagicMock()

    query.filter.return_value.first.return_value = None
    session.query.return_value = query

    with pytest.raises(WrongSecretToken) as exc_info:
        service = ValidateEmail(session,  {"Authorization": "Bearer UnstrustedToken"},fake.email())
        service.execute()

    assert not session.query.called
    assert exc_info.value.code == 401
    assert exc_info.value.description == "El secret token no corresponde"