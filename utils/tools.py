import datetime
import uuid
import os
import csv as CSV
import time
from functools import wraps

NULL_LIST = ["", " ", None, "nan", "NaN", "None", "null", [], {}]


def is_null(value):
    """
    Check if a value is null or not.
    :param value: string or any other value
    :return: boolean
    """
    if value not in NULL_LIST:
        isnull_result = False
    else:
        isnull_result = True
    return isnull_result


def csv(project_name, file_name):
    """
    :param project_name:
    :param file_name:
    :return:
    """
    file = os.path.join(project_path(), 'Project', project_name, 'TestData', file_name)
    print(file)
    r = []
    with open(f'{file}.csv', 'r', encoding='utf-8') as f:
        reader = CSV.reader(f)
        reader.__next__()
        for row in reader:
            r.append(row)
    return r


def get_uuid():
    return "".join(str(uuid.uuid4()).split("-"))


def time_diff_stamp(start_time, end_time):
    start_date = datetime.datetime.fromtimestamp(start_time)
    end_date = datetime.datetime.fromtimestamp(end_time)
    diff = end_date - start_date
    hours = int(diff.seconds / 3600)
    minutes = int((diff.seconds % 3600) / 60)
    seconds = diff.seconds % 60
    return "{} hours, {} minutes, {} seconds".format(hours, minutes, seconds)


def project_path():
    return os.path.dirname(os.path.dirname(__file__))


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)
        return True
    else:
        return False


def get_methods(cls):
    return (list(filter(lambda x: not x.startswith("_") and callable(getattr(cls, x)), dir(cls))))


def retry(retry_limit=3, interval=1):
    def try_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try_count = 0
            res = True
            while try_count < retry_limit:
                res = func(*args, **kwargs)
                if res:
                    break
                else:
                    try_count += 1
                    time.sleep(interval)
            assert res, "Failed to execute the function after {} retries".format(retry_limit)

        return wrapper

    return try_func


if __name__ == '__main__':
    print(project_path())
    res = csv('demo_web', 'test_data')
    print(res)
