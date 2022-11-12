from pathos.pools import ProcessPool as Pool
import time
from loguru import logger

pool = Pool(nodes=4)


def calc(x, y):
    res = x * y
    logger.info("x {}, y {}, res {}", x, y, res)
    time.sleep(4)
    return res


logger.info("before call amap")
pool.amap(calc, [2], [3])
pool.amap(calc, [4], [3])
logger.info("after call amap")
time.sleep(10)
logger.info("after sleep")
