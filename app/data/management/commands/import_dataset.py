from pathlib import Path

from data.importer import import_all, import_file
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import listings from a CSV file into the Listing table."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            type=str,
            required=False,
            help="Path to the CSV file.",
        )

    def handle(self, *args, **options):
        path = options["path"]

        if path:
            import_file(Path(path).resolve())
        else:
            import_all()
