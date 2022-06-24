import sqlite3
from datetime import datetime, timedelta, timezone

class Database:
  def __init__(self, file):
    print("POLLER_DB_FILE: {}".format(file))
    self.file = file
    self.conn = sqlite3.connect(self.file)
    self.cur = self.conn.cursor()
      

  def initialize(self):
    conn = self.conn
    c = self.cur
    schema_switches = """
      CREATE TABLE IF NOT EXISTS switches (
        id integer PRIMARY KEY,
        name text NOT NULL,
        ip_addr text,
        timestamp integer,
        port text,
        port_name text,
        status text,
        vlan text,
        duplex text,
        speed text,
        type text,
        fc_mode text
      )
      """
    c.execute(schema_switches)
    conn.commit

  def store_stat(self, stat, ts):
    conn = self.conn
    c = self.cur
    cols = ', '.join(stat.keys())
    vals = '"' + '", "'.join(stat.values()) + '"'
    store_stat = "INSERT INTO switches ( timestamp, {} ) VALUES( {}, {} );"
    c.execute(store_stat.format(cols, ts, vals))
    conn.commit()

  def duplicate_exist(self, port):
    conn = self.conn
    c = self.cur
    p = """name='{name}' AND 
      ip_addr='{ip_addr}' AND 
      port='{port}' AND 
      port_name='{port_name}' AND 
      status='{status}' AND 
      vlan='{vlan}' AND 
      duplex='{duplex}' AND 
      speed='{speed}' AND 
      type='{type}' AND 
      fc_mode='{fc_mode}'"""
    query = "SELECT COUNT(*) FROM switches WHERE " + p.format(**port)
    result = c.execute(query).fetchone()[0]
    if result > 0:
      return True
    else:
      return False

  def prune_stat(self, days):
    conn = self.conn
    c = self.cur
    now = datetime.now(timezone.utc)
    ts = int((now - timedelta(days)).timestamp())
    query = "DELETE FROM switches WHERE timestamp < {}".format(ts)
    c.execute(query)
    conn.commit()