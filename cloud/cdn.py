# Path: cloud/cdn.py
import requests
import json


class CDN:
    """
    A class that represents a CDN (Content Delivery Network) object. This class is used to upload and download
    files from cloudflare.

    dict reply from cloudflare format example:

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

    def get_link(self, image_id: str) -> dict:
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


def main():
    cdn = CDN()
    cdn.upload()


if __name__ == "__main__":
    main()
