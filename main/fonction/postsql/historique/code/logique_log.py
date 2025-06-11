from datetime import datetime
import os


LOG_DIR = os.path.join(os.path.dirname(__file__), 'historique')
LOG_FILE = os.path.join(LOG_DIR, f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def migrations_write_log(message):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{now} - {message}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message)

def log_and_print(message):
    print(message)
    migrations_write_log(message)

def migrations():
    log_message = "Début de la migration"
    migrations_write_log(log_message)