import logging
import os
import logging.config
from logging.handlers import SocketHandler
import pythonjsonlogger.jsonlogger
from src import logcolor

# Ensure logs directory exists relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(script_dir, 'src', 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, 'app.log').replace('\\', '/')
logging.config.fileConfig(os.path.join(script_dir, "src", "logging.ini"), defaults={'logfilename': log_file_path}, disable_existing_loggers=True)
log = logging.getLogger(__name__)
try:
    socket_handler = SocketHandler("127.0.0.1", 19996)
except:
    pass
log.addHandler(socket_handler)
