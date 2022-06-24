import mysql.connector
import socket
import time
from datetime import datetime, timedelta, timezone

class Database(object):
  def __init__(self, db_config):
    self.host = db_config['host']
    self.port = 3306
    while(self.__port_open() is not True):
      time.sleep(3)
    self.conn = mysql.connector.connect(**db_config)
    self.cur = self.conn.cursor()

  def __port_open(self):
    print("Waiting for DB...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((self.host, self.port))
    if result == 0:
      return True
    else:
      return False

  def initialize(self):
    conn = self.conn
    c = self.cur
    schema_switches = """
      CREATE TABLE IF NOT EXISTS switches (
        id int NOT NULL AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        ip_addr VARCHAR(255),
        timestamp int,
        port VARCHAR(255),
        port_name VARCHAR(255),
        status VARCHAR(255),
        vlan VARCHAR(255),
        duplex VARCHAR(255),
        speed VARCHAR(255),
        type VARCHAR(255),
        fc_mode VARCHAR(255),
        PRIMARY KEY (id)
      )
      """
    c.execute(schema_switches)
    conn.commit

  def store_stat(self, stat, ts):
    conn = self.conn
    c = self.cur
    cols = ', '.join(stat.keys())
    vals = '"' + '", "'.join(stat.values()) + '"'
    store_stat = "INSERT INTO switches ( timestamp, {} ) VALUES( {}, {} );".format(cols, ts, vals)
    c.execute(store_stat)
    conn.commit()

  def prune_stat(self, days):
    conn = self.conn
    c = self.cur
    now = datetime.now(timezone.utc)
    ts = int((now - timedelta(days)).timestamp())
    query = "DELETE FROM switches WHERE timestamp < {}".format(ts)
    c.execute(query)
    conn.commit()
    