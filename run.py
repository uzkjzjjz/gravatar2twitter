import os
import base64
import hashlib

from TwitterAPI import TwitterAPI
import requests

consumer_key = os.getenv('INPUT_CONSUMER_KEY')
assert consumer_key
consumer_secret = os.getenv('INPUT_CONSUMER_SECRET')
assert consumer_secret
key = os.getenv('INPUT_KEY')
assert key
secret = os.getenv('INPUT_SECRET')
assert secret
proxy = os.getenv('INPUT_PROXY')
if proxy:
    os.setenv('http_proxy', proxy)
    os.setenv('https_proxy', proxy)
email = os.getenv('INPUT_EMAIL')
path = os.getenv('INPUT_IMAGE_PATH')
assert email or path


def get_gravatar(email: str):
    email = email.strip().lower()
    uid = hashlib.md5(email.encode()).hexdigest()
    url = f'https://www.gravatar.com/avatar/{uid}?s=400&d=retro'
    return requests.get(url).content


if path:
    with open(path, 'rb') as f:
        image = f.read
else:
    image = get_gravatar(email)

api = TwitterAPI(consumer_key, consumer_secret, key, secret)


def put_avatar(image: bytes):
    res = api.request('account/update_profile_image', {'image': base64.b64encode(image)})

    if res.status_code != 200:
        print(f'Failed to update profile image with status code {res.status_code}')
    else:
        print('OK to update profile image')


put_avatar(image)
