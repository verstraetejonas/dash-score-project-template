import os
import dash_bootstrap_components as dbc

EXTERNAL_STYLESHEETS = [
    dbc.themes.BOOTSTRAP
]
EXTERNAL_SCRIPTS = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js',
]

CACHE_TYPE = 'filesystem'
CACHE_LOCATION = 'cache-directory'
CACHE_TIMEOUT = 60

DEBUG = os.getenv('DEBUG', None) is None

DEFAULT_URL = '/drukte/parking'

