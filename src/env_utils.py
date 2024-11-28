import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent  # This goes up to project root
env_path = BASE_DIR / '.env'  # Look for .env in project root

# Load environment variables
load_dotenv(dotenv_path=env_path, override=True)

# Database settings
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '5440')

# AWS settings
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# Django settings
DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DJANGO_DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'