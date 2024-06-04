from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)

def upload_to_storage(filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket('shopkeeper-sales-data')
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    uploaded_file.save(filename)
    upload_to_storage(filename)
    return "File uploaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)
