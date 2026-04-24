import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pythonjsonlogger import jsonlogger

def init_logger(log_path: str, debug: bool = False):
    #memastikan direktori log tersedia
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("EduPulse-AI")
    
    # Set Level
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)

    # Menghapus handler lama jika ada (mencegah duplikasi log saat reload)
    if logger.hasHandlers():
        logger.handlers.clear()

    #Nama file dengan format tanggal 
    current_date = datetime.now().strftime("%Y%m%d")
    full_path = f"{log_path}{current_date}.log"

    # File Sink dengan Rotasi (10MB per file, max 7 file backup)
    file_handler = RotatingFileHandler(
        full_path, 
        maxBytes=10*1024*1024, # 10MB
        backupCount=7
    )
    
    # Encoder Config (JSON untuk Prod, Console untuk Debug)
    if debug:
        # Format Console yang mudah dibaca untuk Debug
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        file_handler.setFormatter(console_formatter)
    else:
        # Format JSON untuk Production 
        json_formatter = jsonlogger.JsonFormatter(
            fmt='%(timestamp)s %(level)s %(name)s %(message)s %(caller)s',
            rename_fields={"timestamp": "@timestamp", "levelname": "level"}
        )
        file_handler.setFormatter(json_formatter)

    # Console Sink 
    console_handler = logging.StreamHandler()
    if debug:
        console_handler.setFormatter(console_formatter)
    else:
        console_handler.setFormatter(json_formatter)

    # Gabungkan ke logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger