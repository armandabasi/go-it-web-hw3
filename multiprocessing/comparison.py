import logging
import time
from multiprocessing import cpu_count, Pool
from threading import Thread

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def multipliers(number) -> list:
    return [n for n in range(1, number + 1) if number % n == 0]


def factorize_single(*number):
    start_time = time.time()
    list_of_multipliers = []
    for num in number:
        list_of_multipliers.append(multipliers(num))
    return time.time() - start_time


def factorize(*numbers):
    start_time = time.time()
    list_of_multipliers = []
    with Pool(cpu_count()) as pool:
        result = pool.map(multipliers, numbers)
        for _ in result:
            list_of_multipliers.append(_)
    return time.time() - start_time


def factorize_async(*numbers):
    start_time = time.time()
    list_of_multipliers = []
    with Pool(cpu_count()) as pool:
        result = pool.map_async(multipliers, numbers)
        for _ in result.get():
            list_of_multipliers.append(_)
    return time.time() - start_time


if __name__ == '__main__':
    map_time = []
    map_async_time = []
    single_time = []
    threads = []
    num_ = (128, 255, 99999, 10651060)
    for _ in range(10):
        map_time.append(factorize_async(128, 255, 99999, 10651060))
        map_async_time.append(factorize_async(128, 255, 99999, 10651060))
        single_time.append(factorize_single(128, 255, 99999, 10651060))

    logger.info(f"Spent time factorize by async: min time: {min(map_async_time)}, max time: {max(map_async_time)}")
    logger.info(f"Spent time factorize by map: min time: {min(map_time)}, max time: {max(map_time)} ")
    logger.info(f"Spent time factorize by single: min time: {min(single_time)}, max time: {max(single_time)}")
    print("Done")