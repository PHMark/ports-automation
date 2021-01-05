import pymongo
import traceback
from scrapy.exceptions import NotConfigured
from twisted.internet import defer
from txmongo.connection import ConnectionPool


class MongodbPipeline(object):
    """
    Pipeline that writes to Mongo Database
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Retrieves scrapy crawler and accesses pipeline's settings"""

        # Get MongoDB URL from settings
        mongo_url = crawler.settings.get('MONGO_DB_URI', None)
        mongo_db = crawler.settings.get('STAGING_PORTS_DB', None)
        mongo_collection = crawler.settings.get('PORTS_TABLE', None)

        config = [mongo_url, mongo_db, mongo_collection]

        # If doesn't exist, disable the pipeline
        if not any(config):
            raise NotConfigured

        # Create the class
        return cls(config)

    def __init__(self, config):
        """Opens a MongoDB connection pool"""

        # Report connection error only once
        self.report_connection_error = True

        mongo_url, mongo_db, mongo_collection = config

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
        except pymongo.errors.OperationFailure:
            if self.report_connection_error:
                logger.error("Can't connect to MongoDB: %s" %
                             self.mongo_url)
                self.report_connection_error = False
        except Exception:
            print(traceback.format_exc())

        # Return the item for the next stage
        defer.returnValue(item)