import logging
from typing import Optional

class LoggerService:
    """Service for configuring and providing logging functionality."""
    
    @staticmethod
    def configure_logger(
        level: int = logging.INFO,
        format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        log_file: Optional[str] = None
    ):
        """Configure the root logger with specified settings.
        
        Args:
            level: Logging level (default: INFO)
            format_str: Log message format
            log_file: Optional file path to save logs
        """
        logging.basicConfig(
            level=level,
            format=format_str,
            filename=log_file
        )
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger with the specified name.
        
        Args:
            name: Name for the logger (typically __name__)
            
        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)