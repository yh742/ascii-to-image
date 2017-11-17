import os
import time
import pyrebase
from dotenv import load_dotenv
from ascii import handle_image_conversion

POLL = True # flag to use for polling
SLEEP = 5 # seconds to wait till next poll

# Start by loading up our credentials
# ref: https://github.com/theskumar/python-dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Setup an instance of the firebase client
# ref: https://github.com/thisbejim/Pyrebase
CONFIG = {
    "apiKey": os.environ.get('API_KEY', None),
    "authDomain": os.environ.get('AUTH_DOMAIN', None),
    "databaseURL": os.environ.get('DATABASE_URL', None),
    "projectId": os.environ.get('PROJECT_ID', None),
    "storageBucket": os.environ.get('STORAGE_BUCKET', None),
    "messagingSenderId": os.environ.get('MESSAGING_SENDER_ID', None),
    "serviceAccount": os.path.join(os.path.dirname(__file__), 'firebase_admin.json')
}

firebase = pyrebase.initialize_app(CONFIG)


def process_image(filepath):
    """Download the file from firebase, and apply a filter to it
    """
    processed_image_filepath = handle_image_conversion(filepath)
    return processed_image_filepath


def download_image(filename):
    """Download an image from firebase to images/
    """
    destination = os.path.join(os.path.dirname(__file__), 'images/' + filename)
    firebase.storage().child(filename).download(destination)
    return destination


def upload_image(resource, filename):
    """Upload a file to firebase
    """
    # if we want to just overwrite the file, we would do
    # .child(resource).put(filename)
    # but we are going to create a new file now
    firebase.storage().child('ascii-' + resource).put(filename)


def get_filename_list():
    """returns a list of file names from firebase
    @returns list of filenames
    """
    files = []
    objs = firebase.storage().child("").list_files()
    for obj in objs:
        files.append(obj.name)
    return files


def poll_firebase_storage():
    """Checks the firebase storage bucket for any 
    """
    files = get_filename_list()

    for obj in files:
        if os.path.isfile( os.path.join(os.path.dirname(__file__), 'images/' + obj) ) or obj.startswith('ascii-'):
            # if we have the file or its a processed file, we skip it
            continue
        
        filepath = download_image(obj)
        processed_image_filepath = process_image(filepath)
        upload_image(obj, processed_image_filepath)


if __name__ == '__main__':
    while POLL:
        poll_firebase_storage()
        time.sleep(SLEEP)