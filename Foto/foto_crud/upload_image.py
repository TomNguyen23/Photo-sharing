import base64
import requests

class ImgurUpload:
    def __init__(self):
        self.url = "https://api.imgur.com/3/image"
        self.headers = {"Authorization ": "Client-ID fbe9deb628a0276"}

    def upload_image_from_image_path(self, image_path):
        with open(image_path, "rb") as file:
            data = file.read()
            base64_data = base64.b64encode(data)

        response = requests.post(self.url, headers=self.headers, data={"image": base64_data})
        url = response.json()["data"]["link"]
        return url
    
    def upload_image_from_file(self, file):
        data = file.read()
        base64_data = base64.b64encode(data)
        response = requests.post(self.url, headers=self.headers, data={"image": base64_data})
        url = response.json()["data"]["link"]
        return url
    
    def upload_image_from_base64(self, base64_data):
        response = requests.post(self.url, headers=self.headers, data={"image": base64_data})
        url = response.json()["data"]["link"]
        return url