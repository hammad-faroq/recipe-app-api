from unittest.mock import patch# to mock the behaviour
from psycopg2 import OperationalError as Psycopg2OpError #another error hwihc we might expect , which might be thrown by the db if we try to connect it when it is not up
from django.core.management import call_command #package to run the custom commands
from django.db.utils import OperationalError #an error which micht ethrown is db is not up and we run the django app
from django.test import SimpleTestCase#Test case inherit class wehn no db is inlovved


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = (
            [Psycopg2OpError] * 2 +
            [OperationalError] * 3 +
            [True]
        )
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)# to check the oyutput with the desied output in test
        patched_check.assert_called_with(databases=['default'])
