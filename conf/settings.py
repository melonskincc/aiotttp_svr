import logging
import os
import sys

debug = True

db = {
    'user': 'root',
    'password': 'Goodj@b!1',
    'port': 3306,
    'db': 'testb'
}
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)
redis_addr = 'redis://127.0.0.1:6379/0'
# postgresql://{user}:{password}@{host}:{port}/{database}
#   postgres://user:pass@host:port/database?option=value`
pg_dsn = "postgres://postgres:Aa1234@192.168.8.101:5432/postgres"
tasks = ['task_a']
base_log_dir = os.path.join(base_dir, 'log')
if not os.path.exists(base_log_dir):
    os.makedirs(base_log_dir)

log_conf = {
    'level': logging.DEBUG,
    'format': '[%(levelname)s][%(name)s][%(asctime)s] %(message)s',
    'filename': 'log/srv_log.log'
}
