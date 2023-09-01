import os
import random
import requests
import time

username = ''
password = ''
api_dev_key = ''


def plain_paste(title, contents):
    login_url = 'https://pastebin.com/api/api_login.php'
    login_data = {
        'api_dev_key': api_dev_key,
        'api_user_name': username,
        'api_user_password': password
    }

    r = requests.post(login_url, login_data)

    api_user_key = r.text

    paste_url = 'https://pastebin.com/api/api_post.php'
    paste_data = {
        'api_paste_name': title,
        'api_paste_code': contents.decode(),
        'api_dev_key': api_dev_key,
        'api_user_key': api_user_key,
        'api_option': 'paste',
        'api_paste_private': 0
    }

    r = requests.post(paste_url, paste_data)
