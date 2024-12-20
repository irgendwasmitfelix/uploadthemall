import sys
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from instagram_api import Client, ClientError
from tkinter import filedialog
from tkinter import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from tiktok_api import TikTokAPI

# API Keys and Permissions for the Platforms
youtube_api_key = os.getenv("YOUTUBE_API_KEY")  # Replace with your actual API key in environment variables
instagram_access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")  # Replace with your actual access token in environment variables
tiktok_access_token = os.getenv("TIKTOK_ACCESS_TOKEN")  # Replace with your actual access token in environment variables

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.youtube_settings = None
        self.instagram_settings = None
        self.tiktok_settings = None
        self.initUI()

    def initUI(self):
        # Create the layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Create the elements
        select_video_button = QPushButton("Select Video")
        select_video_button.clicked.connect(self.selectVideo)
        upload_video_button = QPushButton("Upload Video")
        upload_video_button.clicked.connect(self.uploadVideo)
        title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        youtube_button = QPushButton("YouTube")
        youtube_button.clicked.connect(self.youtubeSettings)
        instagram_button = QPushButton("Instagram")
        instagram_button.clicked.connect(self.instagramSettings)
        tiktok_button = QPushButton("TikTok")
        tiktok_button.clicked.connect(self.tiktokSettings)

        # Add the elements to the layout
        layout.addWidget(select_video_button, 0, 0)
        layout.addWidget(upload_video_button, 0, 1)
        layout.addWidget(title_label, 1, 0)
        layout.addWidget(self.title_input, 1, 1)
        layout.addWidget(youtube_button, 2, 0)
        layout.addWidget(instagram_button, 2, 1)
        layout.addWidget(tiktok_button, 3, 0)

        self.setWindowTitle("Video Uploader")
        self.show()

    def selectVideo(self):
        # File selection dialog to choose a video from the hard drive
        self.video_path = filedialog.askopenfilename(initialdir="/", title="Select Video", filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))

    def uploadVideo(self):
        # Upload the video to the selected platforms
        title = self.title_input.text()
        youtube_settings = self.youtube_settings
        instagram_settings = self.instagram_settings
        tiktok_settings = self.tiktok_settings

        # YouTube
        if youtube_settings:
            youtube_client = build("youtube", "v3", developerKey=youtube_api_key)
            request = youtube_client.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": youtube_settings["description"],
                        "tags": youtube_settings["tags"],
                        "categoryId": youtube_settings["category"]
                    },
                    "status": {
                        "privacyStatus": youtube_settings["privacy"]
                    }
                },
                media_body=self.video_path
            )
            try:
                response = request.execute()
                print("Video uploaded: https://www.youtube.com/watch?v=" + response["id"])
            except Exception as e:
                print("Error uploading to YouTube:", str(e))

        # Instagram
        if instagram_settings:
            instagram_client = Client(access_token=instagram_access_token)
            try:
                instagram_client.upload_video(self.video_path, caption=instagram_settings["caption"])
                print("Video uploaded: https://www.instagram.com/p/xxxxxx")
            except ClientError as e:
                print("Error uploading to Instagram:", str(e))

        # TikTok
        if tiktok_settings:
            tiktok_client = TikTokAPI(access_token=tiktok_access_token)
            try:
                tiktok_client.upload_video(self.video_path, caption=tiktok_settings["caption"])
                print("Video uploaded: https://www.tiktok.com/@username/video/xxxxxx")
            except Exception as e:
                print("Error uploading to TikTok:", str(e))

    def youtubeSettings(self):
        # Implement YouTube-specific settings dialog here
        # ...

    def instagramSettings(self):
        # Implement Instagram-specific settings dialog here
        # ...

    def tiktokSettings(self):
        # Implement TikTok-specific settings dialog here
        # ...

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
