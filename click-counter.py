import requests
import sys
import argparse
from dotenv import load_dotenv
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'link',
        type=str,
        help='put your linke here'
    )
    return parser.parse_args()


def make_bitlink(token, url):
    headers = {'Authorization': token}
    payload = {'long_url': url}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json=payload)
    if response.ok:
        return response.json()['id']


def count_clicks(token, bit_link):
    headers = {'Authorization': token}
    response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(bit_link), headers=headers)
    if response.ok:
        return response.json()['total_clicks']


if __name__ == '__main__':
    load_dotenv()
    key = os.getenv('BITLY_KEY')
    income_url = parse_args().link
    if income_url.startswith('bit.ly'):
        try:
            click_count = count_clicks(key, income_url)
        except requests.exceptions.HTTPError:
            sys.exit('Неверный URL')
        print(click_count)
    else:
        try:
            bitlink = make_bitlink(key, income_url)
        except requests.exceptions.HTTPError:
            sys.exit('Неверный URL')
        print(bitlink)
