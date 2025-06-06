import oracledb
import os
import configparser
import traceback
import sys
from glootil import DynEnum
from enum import Enum
import logging

oracledb.defaults.fetch_lobs = False
logger = logging.getLogger("oracle")


class OracleDriverAdapter:
    def __init__(self):
        pass

    def select_one(self, *args, **kwargs):
        logger.info("select_one called")
        return None

    def select_many(self, *args, **kwargs):
        logger.info("select_many called")
        return None

    def select_cursor(self, *args, **kwargs):
        logger.info("select_cursor called")
        return None

    def execute(self, *args, **kwargs):
        logger.info("execute called")
        return None

    def process_sql(self, query_fqn, qop, sql):
        logger.info(f"process_sql called: {query_fqn}")
        return sql


def to_query_arg(val):
    if isinstance(val, DynEnum):
        return val.name
    elif isinstance(val, Enum):
        return val.value
    elif val is None:
        return ""
    else:
        return val


class Oracle:
    def __init__(self, path):
        config = configparser.ConfigParser()
        config.read(path)

        username = config.get("oracle", "username")
        password = config.get("oracle", "password")
        wallet_path = config.get("oracle", "wallet_path")
        wallet_password = config.get("oracle", "wallet_password")
        dsn = config.get("oracle", "dsn")
        self.schema = config.get("oracle", "schema")
        os.environ["TNS_ADMIN"] = wallet_path

        self.connection_params = {
            "user": username,
            "password": password,
            "dsn": dsn,
            "wallet_location": wallet_path,
            "wallet_password": wallet_password,
        }
        self.connect()

    def connect(self):
        self.conn = oracledb.connect(**self.connection_params)

    def cursor(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"ALTER SESSION SET CURRENT_SCHEMA = {self.schema}")
        except oracledb.Error as e:
            logger.error(f"Error getting cursor: {e}")
            self.connect()
            cursor = self.conn.cursor()
        return cursor

    def run_query(self, query, **params):
        cols = []
        rows = []
        try:
            cursor = self.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cols = [col[0].lower() for col in cursor.description]
            cursor.close()
        except Exception as e:
            logger.error(f"Error: {e}", e)
            logger.error(traceback.format_exc())

        return cols, rows

    def run(self, query, data=None):
        try:
            cursor = self.cursor()
            if data is not None:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            cursor.close()
        except Exception as e:
            logger.error(f"Error: {e}", e)
            logger.error(traceback.format_exc())

    def select_as_dict(self, query, **params):
        results = []
        cols, rows = self.run_query(query, **params)
        for row in rows:
            row_dict = dict(zip(cols, row))
            results.append(row_dict)
        return results

    def close(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    config_path = sys.argv[1]
    query = sys.argv[2]

    oracle = Oracle(config_path)
    cols, rows = oracle.select_as_dict(query)
    logger.info(cols, rows)
    oracle.close()
