import requests
import pytz
import datetime
import argparse


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('final_check_time', type=int, help='Time checking boundary')
    args = parser.parse_args()
    return args


def load_attempts(devman_api_url):
    params = {'page': 1}
    response = requests.get(
        devman_api_url, params=params).json()
    number_of_pages = response['number_of_pages'] + 1
    solution_attempts = response['records']
    for page in range(2, number_of_pages):
        params['page'] = page
        solution_attempts.extend(requests.get(
            devman_api_url, params=params).json()['records'])
        for attempt in solution_attempts:
            yield {
                'username': attempt['username'],
                'timestamp': attempt['timestamp'],
                'timezone': attempt['timezone'],
            }


def is_timestamp_midnight(timestamp, timezone, final_check_time):
    time = datetime.datetime.fromtimestamp(timestamp)
    local_timezone = pytz.timezone(timezone)
    time_utc_attempt = pytz.utc.localize(time)
    local_time_attempt = time_utc_attempt.astimezone(local_timezone)
    return local_time_attempt.hour >= 0 and local_time_attempt.hour <= final_check_time


def get_midnighters(attempt, final_check_time):
    timestamp = attempt['timestamp'] if attempt['timestamp'] else 0
    timezone = attempt['timezone']
    if is_timestamp_midnight(timestamp, timezone, final_check_time):
        yield attempt['username']


if __name__ == '__main__':
    args = get_console_arguments()
    final_check_time = args.final_check_time
    devman_api_url = 'https://devman.org/api/challenges/solution_attempts'
    attempts = load_attempts(devman_api_url)
    for attempt in attempts:
        midnighters = get_midnighters(attempt, final_check_time)
        for midnighter in midnighters:
            print(midnighter)
