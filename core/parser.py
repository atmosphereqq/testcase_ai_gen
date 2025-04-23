import yaml
import json
from typing import Dict, Any

class SwaggerParser:
    def __init__(self, swagger_file: str):
        """Initialize parser with Swagger file path"""
        self.swagger_file = swagger_file
        self.spec = None
        
    def load_spec(self) -> Dict[str, Any]:
        """Load and parse Swagger/OpenAPI specification"""
        with open(self.swagger_file, 'r') as f:
            if self.swagger_file.endswith('.yaml') or self.swagger_file.endswith('.yml'):
                self.spec = yaml.safe_load(f)
            else:  # assume JSON
                self.spec = json.load(f)
        return self.spec
    
    def parse_paths(self) -> Dict[str, Dict]:
        """Extract all API paths and their methods"""
        if not self.spec:
            self.load_spec()
        return self.spec.get('paths', {})
    
    def parse_parameters(self, path: str, method: str) -> Dict[str, Any]:
        """Parse parameters for a specific path and method"""
        path_item = self.parse_paths().get(path, {})
        method_item = path_item.get(method.lower(), {})
        
        parameters = []
        # Get path-level parameters
        parameters.extend(path_item.get('parameters', []))
        # Get method-level parameters
        parameters.extend(method_item.get('parameters', []))
        
        # Handle requestBody parameters
        body_params = []
        if 'requestBody' in method_item:
            content = method_item['requestBody'].get('content', {})
            for media_type, media_schema in content.items():
                if 'schema' in media_schema and 'properties' in media_schema['schema']:
                    for prop_name, prop_schema in media_schema['schema']['properties'].items():
                        body_params.append({
                            'name': prop_name,
                            'in': 'body',
                            'required': prop_name in media_schema['schema'].get('required', []),
                            'type': prop_schema.get('type', 'string'),
                            'minimum': prop_schema.get('minimum'),
                            'maximum': prop_schema.get('maximum'),
                            'minLength': prop_schema.get('minLength'),
                            'maxLength': prop_schema.get('maxLength'),
                            'enum': prop_schema.get('enum')
                        })
        
        return {
            'path_params': [p for p in parameters if p.get('in') == 'path'],
            'query_params': [p for p in parameters if p.get('in') == 'query'],
            'header_params': [p for p in parameters if p.get('in') == 'header'],
            'body_params': body_params
        }
    
    def parse_responses(self, path: str, method: str) -> Dict[str, Any]:
        """Parse response definitions for a specific path and method"""
        path_item = self.parse_paths().get(path, {})
        method_item = path_item.get(method.lower(), {})
        return method_item.get('responses', {})
