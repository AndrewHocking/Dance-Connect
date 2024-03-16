# Path: cloud/cdn.py
import requests
import json
import uuid
import os
import shutil


class CDN:
    """
    A class that represents a CDN (Content Delivery Network) object. This class is used to upload and download
    files from cloudflare.

    Notes:
    I did not implement List images V2 because we should never need to list all images in the CDN. If we do and there is a
    lot of pictues, then it could cause unessesary load on the server.

    Methods:
        upload: Uploads a file to cloudflare's image CDN.
        download: Downloads a file from cloudflare's image CDN.

    Attributes:
        _key (str): The key used to authenticate with cloudflare's image CDN.
        _account_hash (str): The account hash used to authenticate with cloudflare's image CDN.
    """

    _key: str
    _account_hash: str

    def __init__(self):
        with open("./secrets/keys.json", "r") as file:
            data = json.load(file)
            self._key = data["cloudflare"]["cdn_key"]
            self._account_hash = data["cloudflare"]["account_hash"]
            file.close()

    def upload(self, path: str = "./cloud/testimage.jpg") -> dict:
        """
        Uploads a file to cloudflare's image CDN.
        To access image ID: ["result"]["id"]
        To access image URL: ["result"]["variants"][0]

        Response example:
        {
        "errors": [],
        "messages": [],
        "result": {
            "filename": "logo.png",
            "id": "107b9558-dd06-4bbd-5fef-9c2c16bb7900",
            "meta": {
            "key": "value"
            },
            "requireSignedURLs": true,
            "uploaded": "2014-01-02T02:20:00.123Z",
            "variants": [
            "https://imagedelivery.net/MTt4OTd0b0w5aj/107b9558-dd06-4bbd-5fef-9c2c16bb7900/thumbnail",
            "https://imagedelivery.net/MTt4OTd0b0w5aj/107b9558-dd06-4bbd-5fef-9c2c16bb7900/hero",
            "https://imagedelivery.net/MTt4OTd0b0w5aj/107b9558-dd06-4bbd-5fef-9c2c16bb7900/original"
            ]
        },
        "success": true
        }

        Args:
            path (str): The path to the file to upload.

        Returns:
            dict: A dictionary containing the response from cloudflare's image CDN.
        """
        # TODO - Add error handling for when the file does not exist.
        # TODO - Add error handling for when the file is not an image.
        # TODO - Add error handling for when the file is too large/unsupported/invalidFormat.
        # https://developers.cloudflare.com/images/upload-images/
        # TODO - create an easier dict to return
        upload_url = "https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1".format(
            account_id=self._account_hash
        )
        header = {
            "Authorization": "Bearer {apiToken}".format(apiToken=self._key),
        }

        file = {
            "file": open("{path_to_image}".format(path_to_image=path), "rb"),
        }

        response = requests.post(upload_url, headers=header, files=file)
        return response.json()

    def delete(self, image_id: str) -> dict:
        """
        Deletes a file from cloudflare's image CDN.

        Response example:
        {
        "errors": [],
        "messages": [],
        "result": {},
        "success": true
        }

        Args:
            image_id (str): The ID of the image to delete.

        Returns:
            dict: A dictionary containing the response from cloudflare's image CDN.
        """
        upload_url = "https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/{image_id}".format(
            account_id=self._account_hash, image_id=image_id
        )
        header = {
            "Authorization": "Bearer {apiToken}".format(apiToken=self._key),
        }
        response = requests.delete(upload_url, headers=header)
        return response.json()

    def get_image_details(self, image_id: str) -> dict:
        """
        Gets a link to a file from cloudflare's image CDN.

        Response example:
        {
        "errors": [],
        "messages": [],
        "result": {
            "filename": "logo.png",
            "id": "107b9558-dd06-4bbd-5fef-9c2c16bb7900",
            "meta": {
            "key": "value"
            },
            "requireSignedURLs": true,
            "uploaded": "2014-01-02T02:20:00.123Z",
            "variants": [
            "https://imagedelivery.net/MTt4OTd0b0w5aj/107b9558-dd06-4bbd-5fef-9c2c16bb7900/thumbnail",
            "https://imagedelivery.net/MTt4OTd0b0w5aj/107b9558-dd06-4bbd-5fef-9c2c16bb7900/hero",
            "https://imagedelivery.net/MTt4OTd0b0w5aj/107b9558-dd06-4bbd-5fef-9c2c16bb7900/original"
            ]
        },
        "success": true
        }

        Args:
            image_id (str): The ID of the image to get the link for.

        Returns:
            dict: A dictionary containing the response from cloudflare's image CDN.
        """
        upload_url = "https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/{image_id}".format(
            account_id=self._account_hash, image_id=image_id
        )
        header = {
            "Authorization": "Bearer {apiToken}".format(apiToken=self._key),
        }
        response = requests.get(upload_url, headers=header)
        return response.json()

    def download_original(self, image_id: str) -> str:
        """
        Downloads the original file from cloudflare's image CDN and saves it within a temporary folder.
        Please delete file in temporary folder after use!!! (CDN.empty_temp_folder())

        Args:
            image_id (str): The ID of the image to download.

        Returns:
            str: The path to the downloaded file.
        """
        # uuid is used to generate a unique file name
        fileName = (
            str(uuid.uuid4()) + self.get_image_details(image_id)["result"]["filename"]
        )

        path = "./cloud/temp/{}".format(fileName)

        upload_url = "https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1/{image_id}/blob".format(
            account_id=self._account_hash, image_id=image_id
        )
        header = {
            "Authorization": "Bearer {apiToken}".format(apiToken=self._key),
        }
        blob = requests.get(upload_url, headers=header)
        print(type(blob.content))

        with open(path, "wb") as bn_fl:
            bn_fl.write(blob.content)
            bn_fl.close()

        return path

    def empty_temp_folder(self):
        """
        Empties the temporary folder used to store downloaded files.

        Returns:
            None
        """
        folder = "./cloud/temp/"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(
                        file_path
                    )  # This will remove a folder and all its contents
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))


def main():
    """
    The main function used for manually testing the CDN class.
    """
    cdn = CDN()
    # cdn.empty_temp_folder()
    # print(cdn.download_original("57ca5a8c-f909-429d-d4cb-4b00b75f6d00"))


if __name__ == "__main__":
    main()


"""
Notes:
https://developers.cloudflare.com/api/operations/cloudflare-images-base-image
https://developers.cloudflare.com/images/upload-images/

"""
