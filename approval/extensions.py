from flask_mongoengine import MongoEngine
from utils import captains_log

LOG = captains_log.get_logger()
db = MongoEngine()