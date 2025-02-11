from flask import Flask, render_template, request, send_file
from backend.video_processor import VideoProcessor
from backend.drive_integration import GoogleDriveIntegration
import os
from flask import Flask, render_template, request
from backend.video_processor import VideoProcessor
from backend.drive_integration import GoogleDriveIntegration
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/outputs"  

# Ensure folders exist locally
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Save uploaded video
        video = request.files["video"]
        video_path = os.path.join(UPLOAD_FOLDER, video.filename)
        video.save(video_path)

        # Extract frames
        video_processor = VideoProcessor(video_path, OUTPUT_FOLDER)
        sampled_frames = video_processor.extract_frames()

        # Upload video and frames to Google Drive
        drive_integration = GoogleDriveIntegration()

        uploads_folder_id = "1p8BCnpoDsSnQAAgSv5d3bVLWgC3IpoM-"  # Add correct ID for uploads folder
        output_folder_id = "1jXko48TTRgHhKba2Vb9KF4eEZ7prfHBN"    # Add correct ID for output folder

        # Upload original video to uploads folder
        drive_integration.upload_to_drive(video_path, uploads_folder_id)

        # Upload extracted frames to output folder
        for frame in sampled_frames:
            print(frame)
            drive_integration.upload_to_drive(frame, output_folder_id)

        return render_template("result.html", frames=list(map(lambda x: x.replace('static/', ''), sampled_frames)))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
