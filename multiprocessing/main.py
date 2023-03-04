import logging
import time

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize(*number):
    start_time = time.time()
    list_of_multipliers = []
    for num in number:
        multipliers = [n for n in range(1, num + 1) if num % n == 0]
        list_of_multipliers.append(multipliers)
    logger.info(f"Spent time to calculating {time.time() - start_time}")
    return list_of_multipliers


if __name__ == '__main__':
    a, b, c, d= factorize(128, 255, 99999, 10651060)
    print(f"a == {a},\nb == {b},\nc == {c},\nd == {d}")



