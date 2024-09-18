import random
import string
from config import Config
from app import app

# short link generator
def generate_short_link(length=app.config['SHORT_LINK_LENGTH']):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))