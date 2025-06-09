import logging

import aiosql

from oracle import Oracle, OracleDriverAdapter, to_query_arg

logger = logging.getLogger("state")


class State:
    def __init__(self, config):
        self.db = Oracle(config)

    def setup(self):
        aiosql.register_adapter("aio_oracle", OracleDriverAdapter)
        self.queries = aiosql.from_path("queries.sql", "aio_oracle")

    def get_query(self, query_name):
        return getattr(self.queries, query_name).sql

    async def run_query(self, query_name, **params):
        query_args = {key: to_query_arg(val) for key, val in params.items()}
        return self.db.select_as_dict(self.get_query(query_name), **query_args)

    async def search(
        self,
        query_name: str = "",
        value: str = "",
        use_fuzzy_matching: bool = True,
        limit: int = 50,
    ):
        if use_fuzzy_matching:
            value = f"%{value}%"
        logger.info("search %s, %s, limit %s", query_name, value, limit)
        query = self.get_query(query_name)
        return self.db.select_as_dict(query, value=value, limit=limit)
