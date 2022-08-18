from datetime import timedelta
from functools import partial
from unittest import mock

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, aware_utcnow

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
def fake_password():
    return Faker().password()


@pytest.fixture
def auto_login_user(db, api_client, password):
    def make_auto_login(user=None):
        if user is None:
            user = UserFactory(password=password)
        response = api_client.login(username=user.username, password=password)
        print(response)
        return api_client, user

    return make_auto_login


@pytest.fixture
def auto_login_user_jwt_response(db, api_client, password):
    def make_auto_login(user=None):
        if user is None:
            user = UserFactory(password=password)
        url = reverse("accounts:login")
        data = {"email": user.email, "password": password}
        response = api_client.post(url, data=data)
        body = response.json()
        if "access" in body:
            api_client.credentials(HTTP_AUTHORIZATION="Bearer %s" % body["access"])
        return response.status_code, body

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
            "user-is-trying-to-do-too-much",
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
def test_login(auto_login_user, password, api_client):
    client, user = auto_login_user()
    url = reverse("accounts:login")
    data = {"email": user.email, "password": password}
    response = api_client.post(url, data=data)
    assert response.status_code == 200
    assert user.is_authenticated is True


@pytest.mark.django_db
def test_logout_response_204(auto_login_user_jwt_response, api_client):
    _, body = auto_login_user_jwt_response()
    data = {"refresh": body["refresh"]}
    response = api_client.post(reverse("accounts:logout"), data)
    assert response.status_code == 204


@pytest.mark.django_db
def test_logout_with_bad_refresh_token_response_400(
    auto_login_user_jwt_response, api_client
):
    _, body = auto_login_user_jwt_response()
    data = {"refresh": "random-bad-refresh-token"}
    response = api_client.post(reverse("accounts:logout"), data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_logout_refresh_token_in_blacklist(auto_login_user_jwt_response, api_client):
    _, body = auto_login_user_jwt_response()
    api_client.post(reverse("accounts:logout"), body)
    token = partial(RefreshToken, body["refresh"])
    with pytest.raises(TokenError):
        token()


@pytest.mark.django_db
def test_access_token_still_valid_after_logout(
    auto_login_user_jwt_response, api_client
):
    _, body = auto_login_user_jwt_response()
    api_client.post(reverse("accounts:logout"), body)
    response = api_client.get(reverse("accounts:profile"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_access_token_invalid_after_an_hour(auto_login_user_jwt_response, api_client):
    _, body = auto_login_user_jwt_response()
    api_client.post(reverse("accounts:logout"), body)
    m = mock.Mock()
    m.return_value = aware_utcnow() + timedelta(minutes=60)
    with mock.patch("rest_framework_simplejwt.tokens.aware_utcnow", m):
        response = api_client.get(reverse("accounts:profile"))
    assert response.status_code == 401


@pytest.mark.django_db
def test_change_password_200(
    auto_login_user_jwt_response, password, fake_password, api_client
):
    auto_login_user_jwt_response()
    response = api_client.put(
        reverse("accounts:change-password"),
        data={
            "old_pw": password,
            "new_pw": fake_password,
            "new_pw_conf": fake_password,
        },
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_change_password_wrong_old_password_400(
    auto_login_user_jwt_response, password, fake_password, api_client
):
    auto_login_user_jwt_response()
    response = api_client.put(
        reverse("accounts:change-password"),
        data={
            "old_pw": "random-old-password",
            "new_pw": fake_password,
            "new_pw_conf": fake_password,
        },
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_change_password_non_matching_new_password_400(
    auto_login_user_jwt_response, password, fake_password, api_client
):
    auto_login_user_jwt_response()
    response = api_client.put(
        reverse("accounts:change-password"),
        data={
            "old_pw": password,
            "new_pw": fake_password,
            "new_pw_conf": "non-matching-new-password",
        },
    )
    assert response.status_code == 400
