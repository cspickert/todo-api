from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db.sqlite3",
    }
}

INSTALLED_APPS = ["todo"]
