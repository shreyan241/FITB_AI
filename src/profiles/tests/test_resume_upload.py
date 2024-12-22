import requests
import os

def test_resume_upload():
    # First, get CSRF token by logging in
    session = requests.Session()
    login_url = 'http://localhost:8000/admin/login/'
    
    # Get the login page first to get CSRF token
    response = session.get(login_url)
    if 'csrftoken' in session.cookies:
        csrftoken = session.cookies['csrftoken']
    else:
        raise Exception("No CSRF token found in cookies")

    # Login
    login_data = {
        'username': 'your_username',
        'password': 'your_password',
        'csrfmiddlewaretoken': csrftoken,
    }
    response = session.post(login_url, data=login_data)
    
    # Now upload resume
    upload_url = 'http://localhost:8000/api/profiles/1/resumes'
    
    # Prepare the file and data
    files = {
        'file': ('resume.pdf', open('path/to/your/resume.pdf', 'rb'), 'application/pdf')
    }
    data = {
        'title': 'My Resume'
    }
    
    # Make the upload request
    headers = {
        'X-CSRFToken': session.cookies['csrftoken']
    }
    
    response = session.post(upload_url, files=files, data=data, headers=headers)
    
    # Check response
    if response.status_code == 200:
        print("Upload successful!")
        print(response.json())
    else:
        print(f"Upload failed with status {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_resume_upload() 