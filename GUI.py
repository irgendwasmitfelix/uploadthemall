import sys
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from instagram_api import Client, ClientError
from tkinter import filedialog
from tkinter import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from tiktok_api import TikTokAPI


# API Keys und Genehmigungen für die Plattformen
youtube_api_key = "xxxxxxx"
instagram_api_key = "xxxxxxx"
tiktok_api_key = "xxxxxxx"

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Erstellen des Layouts
        layout = QGridLayout()
        self.setLayout(layout)

        # Erstellen der Elemente
        select_video_button = QPushButton("Video auswählen")
        select_video_button.clicked.connect(self.selectVideo)
        upload_video_button = QPushButton("Video hochladen")
        upload_video_button.clicked.connect(self.uploadVideo)
        title_label = QLabel("Titel:")
        self.title_input = QLineEdit()
        youtube_button = QPushButton("YouTube")
        youtube_button.clicked.connect(self.youtubeSettings)
        instagram_button = QPushButton("Instagram")
        instagram_button.clicked.connect(self.instagramSettings)
        tiktok_button = QPushButton("TikTok")
        tiktok_button.clicked.connect(self.tiktokSettings)

        # Hinzufügen der Elemente zum Layout
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
        # Dateiauswahldialog zum Auswählen eines Videos von der Festplatte
        self.video_path = filedialog.askopenfilename(initialdir = "/", title = "Video auswählen", filetypes = (("mp4 files","*.mp4"),("all files","*.*")))

def uploadVideo(self):
        # Hochladen des Videos auf die ausgewählten Plattformen
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
            response = request.execute()
            print("Video hochgeladen: https://www.youtube.com/watch?v=" + response["id"])

        # Instagram
        if instagram_settings:
            instagram_client = InstagramAPI(access_token=instagram_api_key)
            instagram_client.upload_video(self.video_path, caption=instagram_settings["caption"])
            print("Video hochgeladen: https://www.instagram.com/p/xxxxxx")

        # TikTok
        # if tiktok_settings:
        #     tiktok_client =  tiktok_client(accesstoken=tiktok_api_key)
        #     tiktok_client.upload_video(self.video_path,)