import os
import shutil

from django.test import TestCase

from django.core.management import call_command
from django.db.utils import OperationalError

from unittest import skip
from unittest.mock import patch


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 6)

    @skip("Permission Errors on Travis")
    def test_template_startapp(self):
        """Test creating customized app"""
        call_command('template_startapp', 'testapp')

        top_dir = os.path.join(os.getcwd(), 'testapp')

        self.assertTrue(os.path.exists(os.path.join(
            top_dir, 'urls.py'
        )))
        self.assertTrue(os.path.exists(os.path.join(
            top_dir, 'serializers.py'
        )))
        self.assertTrue(os.path.exists(os.path.join(
            top_dir, 'tests'
        )))
        self.assertTrue(os.path.exists(os.path.join(
            top_dir, os.path.join(
                'tests', '__init__.py'
            )
        )))

        shutil.rmtree(top_dir)
