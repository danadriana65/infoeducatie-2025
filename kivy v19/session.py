import json
import os

class UserSession:
    FILE_NAME = "user_session.json"

    def __init__(self):
        self.username = ""
        self.email = ""
        self.profile_picture = ""
        self.logged_in = False

    def is_complete(self):
        return bool(self.username and self.email)

    def set_profile(self, username, email, image_path=""):
        self.username = username
        self.email = email
        self.profile_picture = image_path
        self.logged_in = True
        self.save()

    def clear(self):
        self.username = ""
        self.email = ""
        self.profile_picture = ""
        self.logged_in = False
        self.save()

    def save(self):
        data = {
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture,
            "logged_in": self.logged_in
        }
        with open(self.FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "r") as f:
                data = json.load(f)
                self.username = data.get("username", "")
                self.email = data.get("email", "")
                self.profile_picture = data.get("profile_picture", "")
                self.logged_in = data.get("logged_in", False)
