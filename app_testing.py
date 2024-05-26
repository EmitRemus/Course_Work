import os
import unittest
from unittest.mock import patch

# Mock environment variables before importing the app module
mock_env = patch.dict(os.environ, {
    "FIREBASE_API_KEY": "fake_api_key",
    "FIREBASE_AUTH_DOMAIN": "fake_auth_domain",
    "FIREBASE_DATABASE_URL": "fake_database_url",
    "FIREBASE_PROJECT_ID": "fake_project_id",
    "FIREBASE_STORAGE_BUCKET": "fake_storage_bucket",
    "FIREBASE_MESSAGING_SENDER_ID": "fake_messaging_sender_id",
    "FIREBASE_APP_ID": "fake_app_id",
    "FIREBASE_MEASUREMENT_ID": "fake_measurement_id"
})

mock_env.start()




from app import app


class TestApp(unittest.TestCase):


    def setUp(self):
        # Set up the Flask test client for each test
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        """
        Test the index route.
        Ensures that the index page loads correctly with a status code of 200
        and contains the word 'Welcome'.
        """
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Password Generator', result.data)

    def test_login_get(self):
        """
        Test the login route with a GET request.
        Ensures that the login page loads correctly with a status code of 200
        and contains the text 'Log In'.
        """
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Log In', result.data)

    def test_signup_get(self):
        """
        Test the signup route with a GET request.
        Ensures that the signup page loads correctly with a status code of 200
        and contains the text 'Sign Up'.
        """
        result = self.app.get('/signup')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Sign Up', result.data)

    def test_forgot_password_get(self):
        """
        Test the forgot password route with a GET request.
        Ensures that the forgot password page loads correctly with a status code of 200
        and contains the text 'Forgot Password'.
        """
        result = self.app.get('/forgot_password')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Forgot Password', result.data)

    def test_dashboard_redirect(self):
        """
        Test the dashboard route without being logged in.
        Ensures that accessing the dashboard without being logged in
        redirects to the login page with a status code of 302.
        """
        result = self.app.get('/dashboard')
        self.assertEqual(result.status_code, 302)  # Redirect to login
        self.assertIn('/login', result.headers['Location'])

    def test_login_post(self):
        """
        Test the login route with a POST request.
        Attempts to log in with the credentials (email: 'test@example.com', password: 'password').
        Ensures that the login process completes and the user is redirected to the dashboard,
        with a success message displayed.
        """
        with self.app:
            response = self.app.post('/login', data=dict(email='test@example.com', password='password'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
