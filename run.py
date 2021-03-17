import sys

# Fix for alpine py3-pillow package
sys.path.append('/usr/lib/python3.8/site-packages')

import os
import base64
import hashlib
import io

from TwitterAPI import TwitterAPI
import requests
from PIL import Image, ImageChops

# Required envs
consumer_key = os.getenv('INPUT_CONSUMER_KEY')
assert consumer_key
consumer_secret = os.getenv('INPUT_CONSUMER_SECRET')
assert consumer_secret
key = os.getenv('INPUT_KEY')
assert key
secret = os.getenv('INPUT_SECRET')
assert secret
name = os.getenv('INPUT_NAME')
assert name
proxy = os.getenv('INPUT_PROXY')

# Optional envs
# Either path or email should be set. Check path first.
if proxy:
    os.setenv('http_proxy', proxy)
    os.setenv('https_proxy', proxy)
email = os.getenv('INPUT_EMAIL')
path = os.getenv('INPUT_IMAGE_PATH')
assert email or path

api = TwitterAPI(consumer_key, consumer_secret, key, secret)


def get_gravatar(email: str):
    email = email.strip().lower()
    uid = hashlib.md5(email.encode()).hexdigest()
    url = f'https://www.gravatar.com/avatar/{uid}?s=400&d=retro'
    return requests.get(url).content


def get_avatar(name: str):
    res = api.request('users/show', {'screen_name': name})

    if res.status_code != 200:
        raise Exception(f'Failed to get profile image with status code {res.status_code}')

    url = res.json()['profile_image_url_https']
    return requests.get(url).content


def put_avatar(image: bytes):
    res = api.request('account/update_profile_image', {'image': base64.b64encode(image)})

    if res.status_code != 200:
        print(f'Failed to update profile image with status code {res.status_code}')
    else:
        print('OK to update profile image')


if path:
    with open(path, 'rb') as f:
        image = f.read
else:
    image = get_gravatar(email)

avatar = get_avatar(name)

image_old = Image.open(io.BytesIO(avatar))
image_new = Image.open(io.BytesIO(image))

diff = ImageChops.difference(image_old, image_new)
if diff.getbbox():
    print('Update avatar')
    put_avatar(image)
else:
    print('No need to update avatar for they are the same')
