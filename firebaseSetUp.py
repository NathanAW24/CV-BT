import os
import firebase_admin
from firebase_admin import credentials

# from google.cloud import firestore
from firebase_admin import storage

# # #print(firestore)
# # #Variables
cred = credentials.Certificate('servacc.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'nuads-mvp1.appspot.com'
})
storagecv = storage.bucket("nuads-cv-headcount")
storage = storage.bucket()

# db = firestore.client()

# from google.cloud import bigquery

# # Construct a BigQuery client object.
# bigqueryclient = bigquery.Client()


# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# # Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': project_id,
# })

# db = firestore.client()