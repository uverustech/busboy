import logging
import sys
from config.settings import settings

def setup_logging():
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Optional: Setup a handler to push logs to Loki (if configured)
    if settings.loki_url:
        try:
            from logging_loki import LokiHandler  # assume you have a custom handler or library
            loki_handler = LokiHandler(
                url=settings.loki_url,
                tags={"app": settings.app_name},
                version="1"
            )
            loki_handler.setLevel(log_level)
            loki_handler.setFormatter(formatter)
            logger.addHandler(loki_handler)
        except ImportError:
            logger.warning("LokiHandler not installed; logs will not be sent to Loki.")
        
    return logger

# Create a global logger instance
logger = setup_logging()

# Usage Example:
if __name__ == "__main__":
    logger.info("Logging is set up and running.")
