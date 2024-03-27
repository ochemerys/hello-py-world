from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from io import BytesIO
import mysql.connector
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from urllib.parse import quote

app = Flask(__name__)

def load_config(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            app.config[key] = value

# Load configuration from text file
load_config('app.config')

# debug_mode = app.config['DEBUG']

# MySQL configurations
db_config = {
    'host': app.config['DB_HOST'],
    'user': app.config['DB_USER'],
    'password': app.config['DB_PASSWORD'],
    'database': app.config['DB_DATABASE']
}

# Azure Storage Account connection string
connection_string = app.config['STORAGE_CONNECTION_STRING']
container_name = app.config['STORAGE_CONTAINER']

# Function to establish MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(**db_config)

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_name(id):
    # Get filename from DB
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM files WHERE id=" + str(id))
        filename = cursor.fetchone()

        if len(filename) == 0 :
            raise ValueError('Wrong file id: {id}.')

        return filename[0]
    except Exception as e:
        raise Exception('Error querying database: {str(e)}')
    finally:
        cursor.close()
        conn.close()
   

# Home page
@app.route('/')
def home():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM files")
        files = cursor.fetchall()
        return render_template('index.html', files=files)
    finally:
        cursor.close()
        conn.close()


# Upload file page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # upload file to Azure
            filepath = container_name
            blob_client = container_client.get_blob_client(filename)
            blob_client.upload_blob(file.stream)
            # Save file info to MySQL database
            try:
                conn = get_mysql_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO files (filename, path) VALUES (%s, %s)', (filename, filepath))
                conn.commit()
            except mysql.connector.Error as err:
                print("MySQL Error:", err)
            finally:
                cursor.close()
                conn.close()
            return redirect(url_for('home'))
    return render_template('upload.html')


# Download file
@app.route("/download/<id>", methods=["GET"])
def download_file(id):
  if request.method == "GET":
    try:
      file_name = get_file_name(id)
      encoded_file_name = quote(file_name)
      blob_client = container_client.get_blob_client(encoded_file_name)
      blob_data = blob_client.download_blob()

      # Set Content-Disposition header to make the browser download the file
      response = send_file(BytesIO(blob_data.readall()),
                         attachment_filename=file_name,
                         as_attachment=True)
      return response
    except Exception as e:
      return jsonify({"error": f"Error downloading blob: {str(e)}"})
  
  return jsonify({"error": "Invalid request method"})


@app.route('/delete/<id>', methods=['DELETE'])
def delete_file(id):
    print(id)
    try:
        file_name = get_file_name(id)
        encoded_file_name = quote(file_name)
        # Delete file from storage
        blob_client = container_client.get_blob_client(encoded_file_name)
        blob_client.delete_blob()
        # Delete file from to MySQL database
        try:
            conn = get_mysql_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM files WHERE id=' + id)
            conn.commit()
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
        finally:
            cursor.close()
            conn.close()
        return f"File '{file_name}' deleted successfully", 200
    except Exception as e:
        print(e)
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)
