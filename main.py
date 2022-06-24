from lib.poller_switches import Poller
import os
import time
from datetime import datetime, timezone

db_type = os.getenv('POLLER_DB_TYPE', 'sqlite')
inventory = os.getenv('POLLER_INVENTORY', 'inventory.yml')
poll_interval = int(os.getenv('POLLER_INTERVAL_MINS', 60))
prune_limit = int(os.getenv('POLLER_PRUNE_LIMIT', 90))

print("POLLER_INTERVAL_MINS: {}".format(str(poll_interval)))
print("POLLER_DB_TYPE: {}".format(db_type))
print("POLLER_INVENTORY: {}".format(inventory))

if db_type == 'sqlite':
  from lib.database_sqlite import Database
  db_file = os.getenv('POLLER_SQLITE_FILE', 'database.db')
  db = Database(db_file)
elif db_type == 'mysql':
  from lib.database_mysql import Database
  db_config = {
    'host': os.getenv('POLLER_MYSQL_HOST', 'localhost'),
    'database': os.getenv('POLLER_MYSQL_DATABASE', 'poller'),
    'user': os.getenv('POLLER_MYSQL_USER', 'poller'),
    'password': os.getenv('POLLER_MYSQL_PASSWORD', 'poller')
  }
  db = Database(db_config)
else:
  print("Invalid database config")
  exit(1)

poller = Poller(inventory)

db.initialize()

while(True):
  print("Initiating poll...")
  db.prune_stat(prune_limit)
  stats = poller.poll_switches()
  ts = str(int(datetime.now(timezone.utc).timestamp()))
  for stat in stats:
    db.store_stat(stat, ts)      
  print("Sleeping for " + str(poll_interval) + " mins")
  time.sleep(poll_interval * 60)