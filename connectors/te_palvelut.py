import os
from dotenv import load_dotenv
import base64

load_dotenv()

username = os.getenv("TE_API_USER", "")
password = os.getenv("TE_API_PASS", "")

def get_auth_header():
    auth = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {auth}"}
