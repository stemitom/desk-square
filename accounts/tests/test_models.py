import pytest
from accounts.models import User
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_model():
    user = UserFactory()
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_user_can_soft_delete():
    user = UserFactory()
    user.delete()
    assert user.deleted_at is not None
    assert User.all_objects.filter(email=user.email).exists()

@pytest.mark.django_db
def test_user_can_restore_after_soft_delete():
    user = UserFactory()
    user.delete()
    assert user.deleted_at is not None
    user.restore()
    assert user.deleted_at is None
    assert User.all_objects.filter(email=user.email).exists()

@pytest.mark.django_db
def test_user_can_hard_delete():
    user = UserFactory()
    user.delete(hard=True)
    assert not (User.all_objects.filter(email=user.email).exists())

