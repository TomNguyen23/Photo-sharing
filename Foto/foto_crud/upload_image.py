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

        # response = requests.post(self.url, headers=self.headers, data={"image": base64_data}, verify=False)
        payload={'type': 'image',
            'title': 'Simple upload',
            'description': 'This is a simple image upload in Imgur'
        }
        files=[
            ('image',('ArtPTXoAAvuny.jpeg',open(image_path,'rb'),'image/jpeg'))
        ]
        headers = {
        'Authorization': 'Client-ID fbe9deb628a0276'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload, files=files)


        # url = response.json()["data"]["link"]
        return response.json()
    
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
    
imgur = ImgurUpload()

# Upload all file in Daniel folder, write the result in Daniel/Daniel.txt
import os
path = "Daniel"
files = os.listdir(path)
with open("Daniel/Daniel.txt", "w") as file:
    for f in files:
        try: 
            file.write(f + " : " + imgur.upload_image_from_image_path(path + "/" + f)['data']['link'] + "\n")
        except:
            continue


