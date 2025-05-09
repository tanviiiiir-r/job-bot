import os
from dotenv import load_dotenv

load_dotenv()

cv_path = os.getenv("CV_FILE", "docs/my_cv.pdf")
my_name = os.getenv("MY_NAME", "John Doe")
my_email = os.getenv("MY_EMAIL", "me@example.com")

def apply_to_job(job_url):
    print(f"📝 Applying to: {job_url}")
    print(f"👤 Name: {my_name}")
    print(f"📧 Email: {my_email}")
    print(f"📄 CV Path: {cv_path}")
    # Add logic here later to actually submit the form or open browser
