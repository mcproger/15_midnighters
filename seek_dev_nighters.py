import requests
import pytz
import datetime
import argparse


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('hours', type=int, help='Time checking boundary')
    args = parser.parse_args()
    return args


def load_attempts(devman_api_url):
    number_of_pages = 11
    attempts = []
    for page in range(1, number_of_pages):
        params = {'page': page}
        response = requests.get(
            devman_api_url, params=params).json()['records']
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
    time_utc_attempt = pytz.utc.localize(time)
    local_time_attempt = time_utc_attempt.astimezone(local_timezone)
    return local_time_attempt.hour >= 0 and local_time_attempt.hour <= hours


def get_midnighters(attempts_info, args):
    for attempt_info in attempts_info:
        timestamp = attempt_info['timestamp'] if attempt_info['timestamp'] else 0
        timezone = attempt_info['timezone']
        if is_timestamp_midnight(timestamp, timezone, args.hours):
            yield attempt_info['username']


if __name__ == '__main__':
    args = get_console_arguments()
    devman_api_url = 'https://devman.org/api/challenges/solution_attempts'
    attempts = load_attempts(devman_api_url)
    attempts_info = get_attempts_info(attempts)
    midnighters = set(get_midnighters(attempts_info, args))
    for midnighter in midnighters:
        print(midnighter)
