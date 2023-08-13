import os

from bson import ObjectId
from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, origins="*")

client = MongoClient("mongodb+srv://farees:Farees123@touchcore.btpzbqa.mongodb.net/")
db = client["touch_core_db"]
collection = db["videos"]

UPLOAD_FOLDER = "uploads"

if not os.path.exists("uploads"):
    os.mkdir("uploads")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


@app.get('/')
def home_page():
    return {"message": "welcome to api"}


@app.post("/upload")
def save_video():
    # Get the file from the request
    file = request.files["video_file"]

    # Check if the file is valid
    if file and any([file.filename.endswith(ext) for ext in [".mkv", ".mp4", ".png"]]):
        # Get a unique ID for the file
        _id = ObjectId()

        # Save the file to the upload folder
        filename = secure_filename(file.filename)
        os.mkdir(f"uploads\\{_id}")
        video_loc = os.path.join(UPLOAD_FOLDER + f"\\{_id}", filename)
        file.save(video_loc)

        # Save the file path to the database
        doc = {"_id": _id, "video_filename": filename, "video_path": video_loc}
        collection.insert_one(doc)
        return {"success": True, "message": "File uploaded successfully!"}
    else:
        return {"success": False, "message": "Invalid file type!"}


@app.get("/videos")
def get_all_videos():
    # Get all files from the database
    videos = collection.find()

    # Create a list of files
    video_list = []
    for v in videos:
        video_list.append({
            "id": str(v["_id"]),
            "video_filename": v["video_filename"],
            "video_path": v["video_path"]
        })

    return video_list


if __name__ == '__main__':
    app.run()
