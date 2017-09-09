import requests
import pytz
import datetime
import argparse


def get_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('hours', type=int)
    args = parser.parse_args()
    return args


def load_attempts():
    number_of_pages = 11
    attempts = []
    for page in range(1, number_of_pages):
        devman_api_url = 'https://devman.org/api/challenges/solution_attempts'
        params = {'page': page}
        response = requests.get(devman_api_url, params=params).json()['records']
        attempts.extend(response)
    return attempts


def get_attempts_info(attempts):
    for attempt in attempts:
        yield {
            'username': attempt['username'],
            'timestamp': attempt['timestamp'],
            'timezone': attempt['timezone'],
        }


def is_timestamp_midnight(timestamp, timezone, hours):
    time = datetime.datetime.fromtimestamp(timestamp)
    local_timezone = pytz.timezone(timezone)
    time_utc = pytz.utc.localize(time)
    local_time = time_utc.astimezone(local_timezone)
    return local_time.hour >= 0 and local_time.hour <= hours 


def get_midnighters(attempts_info):
    pass


if __name__ == '__main__':
    args = get_argparser()
    attempts = load_attempts()
    attempts_info = get_attempts_info(attempts)
    for attempt_info in attempts_info:
        timestamp = attempt_info['timestamp'] if attempt_info['timestamp'] else 0
        timezone = attempt_info['timezone']
        if is_timestamp_midnight(timestamp, timezone, args.hours):
            print(attempt_info['username'])
