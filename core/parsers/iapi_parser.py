from abc import ABC, abstractmethod
from typing import Dict, Any

class IApiParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse API definition file and return standardized format"""
        pass

    @abstractmethod
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file"""
        pass


class ApiDefinition:
    def __init__(self):
        self.endpoints = []
        self.models = {}

    def add_endpoint(self, method: str, path: str, parameters: Dict, responses: Dict):
        self.endpoints.append({
            'method': method,
            'path': path,
            'parameters': parameters,
            'responses': responses
        })

    def add_model(self, name: str, schema: Dict):
        self.models[name] = schema
