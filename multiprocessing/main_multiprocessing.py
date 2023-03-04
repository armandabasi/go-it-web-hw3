import logging
import time
from multiprocessing import cpu_count, Pool

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def multipliers(number) -> list:
    return [n for n in range(1, number + 1) if number % n == 0]


def factorize(*numbers):
    start_time = time.time()
    list_of_multipliers = []
    with Pool(cpu_count()) as pool:
        result = pool.map(multipliers, numbers)
        for _ in result:
            list_of_multipliers.append(_)
    logger.info(f"Spent time to calculating factorize by map  {time.time() - start_time}")
    return list_of_multipliers


if __name__ == '__main__':
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(f"a == {a},\nb == {b},\nc == {c},\nd == {d}")

