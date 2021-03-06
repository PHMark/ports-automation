# data_pipeline/scraper/unece_ports/pipelines/mongodb/__init__.py


import traceback
from scrapy.exceptions import NotConfigured
from twisted.internet import defer
from txmongo.connection import ConnectionPool


class TransactionError(Exception):
    """Raises when mongodb transaction occur."""


class MongodbPipeline(object):
    """
    Pipeline that writes to Mongo Database
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Retrieves scrapy crawler and accesses pipeline's settings"""

        # Get MongoDB URL from settings
        mongo_url = crawler.settings.get('MONGO_DB_URI', None)
        mongo_db = crawler.settings.get('STAGING_DB', None)
        mongo_collection = crawler.settings.get('TABLE_PORTS', None)

        config = [mongo_url, mongo_db, mongo_collection]

        # If doesn't exist, disable the pipeline
        if not any(config):
            raise NotConfigured('Mongodb parameters not configured')

        # Create the class
        return cls(config)

    def __init__(self, config):
        """Opens a MongoDB connection pool"""

        # Report connection error only once
        self.report_connection_error = True

        mongo_url, mongo_db, mongo_collection = config
        if 'mongo:' in mongo_url:
            mongo_url = mongo_url.replace('mongo:', 'mongodb:')
        # Setup MongoDB Connection
        self.mongo_url = mongo_url
        self.connection = ConnectionPool(mongo_url, connect_timeout=5)
        self.mongo_db = self.connection[mongo_db]
        self.collection = self.mongo_db[mongo_collection]

    def close_spider(self, spider):
        """Discard the database on spider close"""
        self.connection.disconnect()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """Processes the item. Does upsert into MongoDB"""
        logger = spider.logger
        try:
            yield self.collection.replace_one(
                filter=item,
                replacement=item,
                upsert=True
            )
        except Exception:
            if self.report_connection_error:
                logger.error("An error occured while Upserting data")
                self.report_connection_error = False
                logger.error(traceback.format_exc())
                raise TransactionError('An error occured during transaction.')

        # Return the item for the next stage
        defer.returnValue(item)
