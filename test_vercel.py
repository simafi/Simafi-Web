import os
import sys

# Ensure backend and api are accessible
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ["DJANGO_DEBUG"] = "1"
os.environ["DJANGO_SECURE_SSL_REDIRECT"] = "0"

from api.index import app
from django.test import RequestFactory

# Create a test request
factory = RequestFactory()

urls = [
    '/tributario/gestionar-mora-bienes/',
    '/tributario/maestro-negocios/',
]

for url in urls:
    request = factory.get(url)
    
    # Process through Vercel's app
    try:
        response = app.get_response(request)
        print(f"URL: {url} - Status: {response.status_code}")
        if response.status_code == 500:
            print(f"Content: {response.content.decode('utf-8')[:500]}")
    except Exception as e:
        print(f"CRASH on {url}: {e}")
        import traceback
        traceback.print_exc()
