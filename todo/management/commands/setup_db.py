from typing import Any

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        # Migrate database.
        self.stdout.write("Migrating database...")
        call_command("migrate")

        # Load fixtures.
        self.stdout.write("Loading fixtures...")
        call_command(
            "loaddata",
            settings.PROJECT_ROOT / "todo/management/commands/data/fixtures.json",
        )

        # Done!
        self.stdout.write(self.style.SUCCESS("Done."))
