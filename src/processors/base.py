from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

class BaseProcessor(ABC):
    """Base class for all processors."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """Process the input data."""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """Validate input data."""
        pass
    
    def pre_process(self, input_data: Any) -> Any:
        """Pre-process steps before main processing."""
        return input_data
    
    def post_process(self, processed_data: Any) -> Any:
        """Post-process steps after main processing."""
        return processed_data
