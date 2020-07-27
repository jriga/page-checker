import argparse
import config
import core
import db
from runner import AsyncRunner
import logging
import functools as ft


loglevel = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET
}

c = {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Site checker")

    parser.add_argument('-c',
                        '--configuration',
                        help="path to configuration file",
                        type=str,
                        default="./config.json")

    parser.add_argument('-u',
                        '--urls',
                        help="list of urls to check",
                        type=str)

    parser.add_argument('-f',
                        '--frequency',
                        help="frequency of checks",
                        type=int,
                        default="60")

    parser.add_argument('-p',
                        '--persist',
                        help="persist in db for change notification",
                        type=str,
                        default="false")

    parser.add_argument('-l',
                        '--log',
                        help="log level",
                        type=str,
                        default="INFO")

    args = parser.parse_args()
    c = config.load(vars(args))

    logging.basicConfig(
        level=loglevel.get(c['log'].upper(), logging.INFO),
        format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )

else:
    c = config.load({"configuration": './config.json'})


runner = AsyncRunner(
    ft.partial(core.checkall, c),
    frequency=c['frequency'])

runner.before_run(
    ft.partial(db.load_database, c))

runner.run()
