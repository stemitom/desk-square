import pytest
from django.urls import reverse

from accounts.tests.factories import UserFactory


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def password():
    return "strong-test-pass"


@pytest.fixture
def auto_login_user(db, client, password):
    def make_auto_login(user=None):
        if user is None:
            user = UserFactory(password=password)
        client.login(username=user.username, password=password)
        return client, user

    return make_auto_login


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse("accounts:profile")
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authorized_request(api_client_with_credentials):
    url = reverse("accounts:profile")
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, email, first_name, last_name, password, status_code",
    [
        (
            "useristryingtodotoomuch",
            "user@example.com",
            "test",
            "user",
            "strong_pass",
            400,
        ),
        ("user", "user@example.com", "test", "user", "weak", 400),
        ("user", "user@example.com", "test", "user", "strong_pass", 201),
    ],
)
def test_signup_data_validation(
    username,
    email,
    first_name,
    last_name,
    password,
    status_code,
    api_client,
):
    url = reverse("accounts:signup")
    data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status_code


@pytest.mark.django_db
def test_login(auto_login_user, password):
    client, user = auto_login_user()
    url = reverse("accounts:login")
    data = {"email": user.email, "password": password}
    response = client.post(url, data=data)
    assert response.status_code == 200
