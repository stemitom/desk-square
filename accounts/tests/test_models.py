from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.models import User


class TestModels(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            email="testuser@gmail.com",
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        User.objects.create(
            email="testuser2@gmail.com",
            username="testuser2",
            first_name="Test2",
            last_name="User2",
        )

    def test_user_creation(self) -> None:
        testuser = User.objects.get(email="testuser@gmail.com")
        self.assertTrue(isinstance(testuser, User))
        self.assertEqual(str(testuser), testuser.email)

    # def test_user_cannot_create_with_case_sensitive_username(self) -> None:
    #     with self.assertRaises(IntegrityError) as ctx:
    #         User.objects.create(email="citestuser1@gmail.com", username="citestuser")
    #         User.objects.create(email="citestuser2@gmail.com", username="ciTestuser")
    #     self.assertEqual(IntegrityError, type(ctx.exception))

    def test_user_can_soft_delete(self) -> None:
        testuser = User.objects.get(email="testuser@gmail.com")
        testuser.delete()
        self.assertIsNotNone(testuser.deleted_at)
        self.assertTrue(User.all_objects.filter(email=testuser.email).exists())

    def test_user_can_restore_after_soft_delete(self) -> None:
        testuser = User.objects.get(email="testuser@gmail.com")
        testuser.delete()
        self.assertIsNotNone(testuser.deleted_at)
        testuser.restore()
        self.assertIsNone(testuser.deleted_at)
        self.assertTrue(User.all_objects.filter(email=testuser.email).exists())

    def test_user_can_be_hard_deleted(self) -> None:
        testuser = User.objects.get(email="testuser@gmail.com")
        testuser.delete(hard=True)
        self.assertFalse(User.all_objects.filter(email=testuser.email).exists())
