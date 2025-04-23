import json
from typing import Dict, Any
from core.parsers.iapi_parser import IApiParser, ApiDefinition

class ApifoxParser(IApiParser):
    def __init__(self):
        self.api_def = None
        
    def can_parse(self, file_path: str) -> bool:
        """Check if file is Apifox format"""
        return file_path.endswith('.json')
        
    def parse(self, file_path: str) -> ApiDefinition:
        """Parse Apifox file into standardized ApiDefinition"""
        self.api_def = ApiDefinition()
        
        with open(file_path, 'r') as f:
            apifox_data = json.load(f)
            
        for interface in apifox_data.get('interfaces', []):
            method = interface.get('method', '').upper()
            path = interface.get('path', '')
            
            if method and path:
                parameters = self._parse_parameters(interface)
                responses = self._parse_responses(interface)
                
                self.api_def.add_endpoint(method, path, parameters, responses)
                
        return self.api_def
        
    def _parse_parameters(self, interface: Dict) -> Dict[str, Any]:
        """Extract parameters from Apifox interface"""
        params = {
            'path_params': [],
            'query_params': [],
            'header_params': [],
            'body_params': []
        }
        
        # Parse path parameters
        for param in interface.get('parameters', []):
            if param.get('in') == 'path':
                params['path_params'].append({
                    'name': param.get('name', ''),
                    'required': param.get('required', False),
                    'type': param.get('type', 'string')
                })
                
        # Parse request body parameters
        request_body = interface.get('requestBody', {})
        content = request_body.get('content', {})
        if 'application/json' in content:
            schema = content['application/json'].get('schema', {})
            if 'properties' in schema:
                for prop_name, prop_schema in schema['properties'].items():
                    params['body_params'].append({
                        'name': prop_name,
                        'required': prop_name in schema.get('required', []),
                        'type': prop_schema.get('type', 'string')
                    })
                    
        return params
        
    def _parse_responses(self, interface: Dict) -> Dict[str, Any]:
        """Parse responses from Apifox interface"""
        responses = {}
        for status_code, response in interface.get('responses', {}).items():
            responses[status_code] = {
                'description': response.get('description', ''),
                'content': response.get('content', {})
            }
        return responses
