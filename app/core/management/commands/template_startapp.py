import os
import shutil

from django.core.management.templates import TemplateCommand


def create_file(directory, file_name, file_content=None):
    """Create customized file"""
    with open(os.path.join(directory, file_name), 'w+') as file:
        if file_content:
            file.write(file_content)


class Command(TemplateCommand):
    """Django command to create a template app"""

    help = (
        "Creates a RestFramework app directory structure for the given app "
        "name in the current directory or optionally in the given directory"
    )
    missing_args_message = "You must provide an application name."

    def handle(self, *args, **options):
        """Command logic"""
        app_name = options.pop('name')
        target = options.pop('directory')

        super().handle('app', app_name, target, **options)

        # All exceptions handled in super().handle(*args) call
        if target is None:
            directory = os.path.join(os.getcwd(), app_name)
        else:
            directory = os.path.abspath(os.path.expanduser(target))

        if os.path.exists(directory):
            # Customize the app created
            # Remove unnecessary content
            files_remove = [
                'admin.py', 'models.py', 'tests.py'
            ]

            for file in files_remove:
                os.remove(os.path.join(directory, file))
            shutil.rmtree(os.path.join(directory, 'migrations'))

            # Add necessary content
            os.mkdir(os.path.join(directory, 'tests'))

            create_file(directory, 'tests/__init__.py')
            create_file(directory, 'urls.py',
                        'from django.urls import path\n\n'
                        f'app_name = \'{app_name}\'\n\n'
                        'urlpatterns = []\n')
            create_file(directory, 'serializers.py',
                        'from rest_framework import serializers\n')

            self.stdout.write(self.style.SUCCESS(
                f'{app_name} has been customized!'
            ))
