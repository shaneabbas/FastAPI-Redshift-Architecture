# Importing Python packages
import asyncpg
import logging


logger = logging.getLogger('foo-logger')


# ----------------------------------------------------------------------------------------------------


class Database:
    def __init__(self, user, password, host, database, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._cursor = None

        self._connection_pool = None
    

    # Connect to postgres db
    async def connect(self):
        if not self._connection_pool:
            try:
                self._connection_pool = await asyncpg.create_pool(
                    min_size=1,
                    max_size=20,
                    command_timeout=60,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    ssl="require"
                )
                logger.info("Database pool connection opened")

            except Exception as e:
                logger.exception(e)


    # Execute query
    async def execute_query(self, query: str, *args):
        if not self._connection_pool:
            await self.connect()
        else:
            con = await self._connection_pool.acquire()
            try:
                result = await con.fetch(query, *args)
                # Convert records to list of dictionaries
                values = [dict(record) for record in result]
                return values
            except Exception as e:
                logger.exception(e)
            finally:
                await self._connection_pool.release(con)


    # Close connection
    async def close(self):
        if not self._connection_pool:
            try:
                await self._connection_pool.close()
                logger.info("Database pool connection closed")
            except Exception as e:
                logger.exception(e)
