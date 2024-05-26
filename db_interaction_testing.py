import base64
import unittest
from unittest.mock import patch, MagicMock
from db_interactions import (get_user_by_email, insert_user, get_user_id,
                             get_encrypted_passwords, insert_password, update_password,
                             delete_password_by_id, get_password_by_id)


class TestDatabaseFunctions(unittest.TestCase):

    @patch('db_interactions.get_db_connection')
    def test_get_user_by_email(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'id': 1, 'mail': 'test@example.com'}

        result = get_user_by_email('test@example.com')
        self.assertEqual(result, {'id': 1, 'mail': 'test@example.com'})
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE mail = %s", ('test@example.com',))

    @patch('db_interactions.get_db_connection')
    def test_insert_user(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        insert_user('test@example.com', 'testuser')
        mock_cursor.execute.assert_called_once_with("INSERT INTO users (mail, name) VALUES (%s, %s)",
                                                    ('test@example.com', 'testuser'))
        mock_connection.commit.assert_called_once()

    @patch('db_interactions.get_db_connection')
    def test_get_user_id(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'id': 1}

        result = get_user_id('test@example.com')
        self.assertEqual(result, 1)
        mock_cursor.execute.assert_called_once_with("SELECT id FROM users WHERE mail = %s", ('test@example.com',))

    @patch('db_interactions.get_db_connection')
    def test_get_encrypted_passwords(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'password_id': 1, 'user_id': 1, 'password': 'encrypted', 'used_for': 'description'}]

        result = get_encrypted_passwords(1)
        self.assertEqual(result, [{'password_id': 1, 'user_id': 1, 'password': 'encrypted', 'used_for': 'description'}])
        mock_cursor.execute.assert_called_once_with("SELECT * FROM passwords WHERE user_id = %s", (1,))

    @patch('db_interactions.get_db_connection')
    def test_insert_password(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        insert_password(1, 'encrypted_password', 'encrypted_description', b'salt', 'iv_password', 'iv_description')
        mock_cursor.execute.assert_called_once_with(
            """INSERT INTO passwords (user_id, password, used_for, salt, iv_password, iv_used_for) VALUES (%s, %s, %s, %s, %s, %s)""".strip(),
            (1, 'encrypted_password', 'encrypted_description', base64.b64encode(b'salt').decode('utf-8'), 'iv_password',
             'iv_description')
        )
        mock_connection.commit.assert_called_once()

    @patch('db_interactions.get_db_connection')
    def test_update_password(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        update_password(1, 'encrypted_password', 'encrypted_description', b'salt', 'iv_password', 'iv_description')
        mock_cursor.execute.assert_called_once_with(
            """UPDATE passwords SET password = %s, used_for = %s, salt = %s, iv_password = %s, iv_used_for = %s WHERE password_id = %s""".strip(),
            ('encrypted_password', 'encrypted_description', base64.b64encode(b'salt').decode('utf-8'), 'iv_password',
             'iv_description', 1)
        )
        mock_connection.commit.assert_called_once()

    @patch('db_interactions.get_db_connection')
    def test_delete_password_by_id(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        delete_password_by_id(1)
        mock_cursor.execute.assert_called_once_with("DELETE FROM passwords WHERE password_id = %s", (1,))
        mock_connection.commit.assert_called_once()

    @patch('db_interactions.get_db_connection')
    def test_get_password_by_id(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'password_id': 1, 'password': 'encrypted', 'used_for': 'description'}

        result = get_password_by_id(1)
        self.assertEqual(result, {'password_id': 1, 'password': 'encrypted', 'used_for': 'description'})
        mock_cursor.execute.assert_called_once_with("SELECT * FROM passwords WHERE password_id = %s", (1,))


if __name__ == '__main__':
    unittest.main()
