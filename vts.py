from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import json

app = Flask(__name__)
# Load the configuration file
with open('config.json') as f:
    config = json.load(f)

# Use a service account to initialize the Firebase Admin SDK
cred = credentials.Certificate(config['FIRESTORE_KEY'])
firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

#set up route homepage (‘/’) accepting GET & POST requests
@app.route('/', methods=['GET', 'POST'])
def mapview():
    vehicle_id = request.form.get('vehicle_id') if request.method == 'POST' else None
    date = request.form.get('date') if request.method == 'POST' else None

    # Get a reference to the collection containing your data
    data_ref = db.collection(str(vehicle_id)) if vehicle_id else db.collection('data')

    # Create a query that orders the results by the TimeStamp field
    query = data_ref.order_by('TimeStamp')

    # Retrieve data from the collection using the query
    data = []
    for doc in query.stream():
        doc_data = doc.to_dict()
        doc_data['TimeStamp'] = datetime.fromtimestamp(doc_data['TimeStamp']).strftime('%Y-%m-%d')
        if date and doc_data['TimeStamp'] != date:
            continue
        data.append(doc_data)

    # Get all collections (i.e., all vehicle_ids)
    collections = [coll.id for coll in db.collections()]

    return render_template('map.html', data=data, collections=collections, mapbox_access_token=config['MAPBOX_ACCESS_TOKEN'])

if __name__ == '__main__':
    app.run(debug=True)
