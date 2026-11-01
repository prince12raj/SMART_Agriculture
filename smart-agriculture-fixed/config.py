import os
import socket
import logging
from urllib.parse import urlparse

log = logging.getLogger(__name__)


def _build_database_uri():
    """Return a usable SQLAlchemy URI.

    - Converts postgres:// to postgresql:// (Render/Heroku style)
    - Adds sslmode=require for hosted Postgres (Supabase etc.)
    - Falls back to local SQLite if the DB host does not resolve,
      so the app keeps working instead of returning 500 errors.
    """
    url = os.environ.get('DATABASE_URL', '').strip()

    if not url:
        return 'sqlite:///agri.db'

    if url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)

    if url.startswith('postgresql'):
        host = urlparse(url).hostname
        try:
            socket.getaddrinfo(host, None)
        except (socket.gaierror, TypeError):
            log.error(
                "DATABASE_URL host %r does not resolve. "
                "Falling back to SQLite. Fix DATABASE_URL in Render.", host
            )
            return 'sqlite:///agri.db'

        if 'sslmode=' not in url and 'localhost' not in url:
            url += ('&' if '?' in url else '?') + 'sslmode=require'

    return url


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'agri-smart-secret-2024')

    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # ML Model paths
    SOIL_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'soil_model.pkl')
    DISEASE_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'disease_model.h5')
    PRICE_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'price_model.pkl')

    # Anthropic API Key
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
