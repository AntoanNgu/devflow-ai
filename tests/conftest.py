import os
from dotenv import load_dotenv

load_dotenv()
url = os.environ["TEST_DATABASE_URL"]
os.environ["DATABASE_URL"] = url 