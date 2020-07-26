import asyncio
import aiohttp
import aiosqlite
import time
import sys
import logging

import db


async def fetch(session, url):
    logging.debug(f'Task fetch for {url}')
    start = time.time()
    try:
        async with session.get(url) as response:
            now = time.time()
            record = db.Record(url, response.status, now - start, now)
            logging.debug(f'found {record}')
            return record
    except:
        logging.exception(f'fetch exception {sys.exc_info()[0]}')


async def persist(db, record, save=False):
    logging.debug(f'Task: persist for {record}')

    def insert_statement(r):
        return f'''INSERT INTO records (url, status, latency, timestamp) 
        VALUES ("{r.url}", {r.status}, {r.latency}, {r.timestamp})'''

    if save:
        logging.debug(f'persisting {record}')
        await db.execute(insert_statement(record))
        await db.commit()
    else:
        logging.debug(f'skipping persist for {record}')


async def report(record):
    logging.debug(f'Task: report for {record}')
    pass


async def worker(session, db, url, save):
    record = await fetch(session, url)
    await persist(db, record, save)
    await report(record)


async def checkall(config):
    logging.debug('In checkall')
    logging.debug(' -- '*30)
    async with aiohttp.ClientSession() as session:
        async with aiosqlite.connect(config['db_path']) as db:
            # launch workers
            await asyncio.gather(
                *(worker(session, db, url, config['persist']) for url in config['urls']))
