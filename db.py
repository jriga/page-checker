import sqlite3
import logging
from collections import namedtuple

schema = '''
CREATE TABLE IF NOT EXISTS records (
  id integer primary key,
  url text,
  status real,
  latency real,
  timestamp datetime)
'''

Record = namedtuple('Record', 'url status latency timestamp')


def load_database(config, sql=sqlite3):
    logging.debug('Create table records if not present')
    try:
        conn = sql.connect(config['db_path'])
        c = conn.cursor()
        c.execute(schema)
        conn.commit()
    except sqlite3.Error as exc:
        logging.exception(f'Error in loading database {exc}')
