import logging
import os

def get_logger(name: str):
    """
    Creates and returns a formatted logger instance.
    """
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S"
        ))

        # File handler
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S"
        ))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
