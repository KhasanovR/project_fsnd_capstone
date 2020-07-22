import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

auth0_config = {
    "AUTH0_DOMAIN": os.environ.get('AUTH0_DOMAIN'),
    "ALGORITHMS": [os.environ.get('ALGORITHMS')],
    "API_AUDIENCE": os.environ.get('API_AUDIENCE')
}

PAGINATION = os.environ.get('PAGINATION')

bearer_tokens = {
    "casting_assistant": "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_TOKEN')),
    "executive_producer": "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_TOKEN')),
    "casting_director": "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_TOKEN'))
}

DATABASE_URL = os.environ.get('DATABASE_URL')
