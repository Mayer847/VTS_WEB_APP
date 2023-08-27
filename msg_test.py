import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Load the config.json file
with open('config.json') as json_file:
    config = json.load(json_file)

# Use a service account to initialize the Firebase Admin SDK
cred = credentials.Certificate(config['FIRESTORE_KEY'])
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

# Open the file containing your data
with open('data.csv', 'r') as file:
    # Create a CSV reader object
    reader = csv.DictReader(file)

    # Iterate over each row in the file
    for row in reader:
        # Set the data you want to add to your database
        data = {
            'TimeStamp': int(row['TimeStamp']),
            'Latitude': float(row['Latitude']),
            'Longitude': float(row['Longitude']),
            'Status': int(row['Status']),
            'Speed': int(row['Speed'])
        }

        # Get a reference to the collection where you want to store your data
        # Use 'NewCollectionName' as the name of the collection
        data_ref = db.collection('f1')

        # Add the data to your Firestore collection
        data_ref.add(data)
