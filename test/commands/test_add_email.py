import pytest
from unittest.mock import patch, MagicMock
from faker import Faker

from src.commands.add_email import AddEmail
from src.commands.constants import Constant
from src.errors.errors import MissingRequiredToken, WrongSecretToken
from src.models.blacklist import BlackList
from test.mock_session import MockSession

fake = Faker()


@pytest.fixture
def mock_session():
    return MockSession()


def create_email_blacklist(session, blacklist_mock):
    return AddEmail(session,
                    {"email": blacklist_mock.email,
                     "app_uuid": blacklist_mock.app_uuid,
                     "blocked_reason": blacklist_mock.blocked_reason},
                    {'Authorization': 'Bearer ' + Constant.SECRET_TOKEN}, blacklist_mock.ip)


def create_email_blacklist_no_header(session, blacklist_mock):
    return AddEmail(session,
                    {"email": blacklist_mock.email,
                     "app_uuid": blacklist_mock.app_uuid,
                     "blocked_reason": blacklist_mock.blocked_reason},
                    {}, blacklist_mock.ip)


def create_email_blacklist_wrong_token(session, blacklist_mock):
    return AddEmail(session,
                    {"email": blacklist_mock.email,
                     "app_uuid": blacklist_mock.app_uuid,
                     "blocked_reason": blacklist_mock.blocked_reason},
                    {'Authorization': 'Bearer whatever'}, blacklist_mock.ip)


def blacklist_mock():
    return BlackList(fake.safe_email(), fake.uuid4(), fake.paragraph(nb_sentences=1), fake.ipv4())


def test_create_email():
    my_blacklist_mock = blacklist_mock()
    session = MagicMock()
    query = MagicMock()
    query.filter.return_value.first.return_value = my_blacklist_mock
    session.query.return_value = query
    add_email_blacklist = create_email_blacklist(session, my_blacklist_mock)
    result = add_email_blacklist.execute()
    assert result == "Se  agregado el email a la lista"


@patch('test.mock_session', autospec=True)
def test_create_email_without_token(mock_session):
    my_blacklist_mock = blacklist_mock()
    with pytest.raises(MissingRequiredToken):
        service = create_email_blacklist_no_header(mock_session, my_blacklist_mock)
        service.execute()


@patch('test.mock_session', autospec=True)
def test_create_email_with_token_invalid(mock_session):
    my_blacklist_mock = blacklist_mock()
    with pytest.raises(WrongSecretToken):
        service = create_email_blacklist_wrong_token(mock_session, my_blacklist_mock)
        service.execute()
