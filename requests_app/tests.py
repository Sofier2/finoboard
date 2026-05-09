from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CitizenProfile


class FinoBoardTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )

    # 1
    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")

    # 2
    def test_user_password_check(self):
        self.assertTrue(self.user.check_password("12345"))

    # 3
    def test_user_login(self):
        login = self.client.login(username="testuser", password="12345")
        self.assertTrue(login)

    # 4
    def test_wrong_login_fails(self):
        login = self.client.login(username="testuser", password="wrong")
        self.assertFalse(login)

    # 5
    def test_profile_creation(self):
        profile = CitizenProfile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)

    # 6
    def test_profile_strong_relation(self):
        profile = CitizenProfile.objects.create(user=self.user)
        self.assertEqual(profile.user.username, "testuser")

    # 7
    def test_home_page_status(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, [200, 302])

    # 8
    def test_admin_page_access_redirect(self):
        response = self.client.get("/admin/")
        self.assertIn(response.status_code, [200, 302])

    # 9
    def test_user_exists_in_db(self):
        self.assertEqual(User.objects.count(), 1)

    # 10
    def test_profile_created_count(self):
        CitizenProfile.objects.create(user=self.user)
        self.assertEqual(CitizenProfile.objects.count(), 1)

    # 11
    def test_user_logout(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get("/logout/")
        self.assertIn(response.status_code, [200, 302])

    # 12
    def test_invalid_user_not_found(self):
        user = User.objects.filter(username="fake").first()
        self.assertIsNone(user)

    # 13
    def test_client_session_active(self):
        self.client.login(username="testuser", password="12345")
        session = self.client.session
        self.assertTrue(session is not None)

    # 14
    def test_database_isolation(self):
        self.assertEqual(User.objects.count(), 1)

    # 15
    def test_profile_delete(self):
        profile = CitizenProfile.objects.create(user=self.user)
        profile.delete()
        self.assertEqual(CitizenProfile.objects.count(), 0)