
import time

from producer import publish
from changed_data import provide_changed_data


if __name__ == '__main__':
    i = 1
    while True:
        print("This prints once in 10 minutes. Ping number: {}".format(i))
        publish('changed_data', {'changed_data': provide_changed_data(),
                                 'S. No.': 'data: {}'.format(i)})
        i += 1
        time.sleep(5)  # Delay for 10 minutes.
