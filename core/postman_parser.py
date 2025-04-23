import json
from typing import Dict, Any
from .iapi_parser import IApiParser, ApiDefinition

class PostmanParser(IApiParser):
    def __init__(self):
        self.api_def = None
        
    def can_parse(self, file_path: str) -> bool:
        """Check if file is Postman collection format"""
        return file_path.endswith('.json')
        
    def parse(self, file_path: str) -> ApiDefinition:
        """Parse Postman collection into standardized ApiDefinition"""
        self.api_def = ApiDefinition()
        
        with open(file_path, 'r') as f:
            collection = json.load(f)
            
        for item in collection.get('item', []):
            request = item.get('request', {})
            method = request.get('method', '').upper()
            url = request.get('url', {})
            path = '/'.join(url.get('path', []))
            
            if method and path:
                # Parse parameters from request
                parameters = self._parse_parameters(request)
                responses = self._parse_responses(item)
                
                self.api_def.add_endpoint(method, path, parameters, responses)
                
        return self.api_def
        
    def _parse_parameters(self, request: Dict) -> Dict[str, Any]:
        """Extract parameters from Postman request"""
        params = {
            'path_params': [],
            'query_params': [],
            'header_params': [],
            'body_params': []
        }
        
        # Parse URL path parameters
        url = request.get('url', {})
        if 'variable' in url:
            for var in url['variable']:
                params['path_params'].append({
                    'name': var.get('key', ''),
                    'required': True,
                    'type': 'string'
                })
                
        # Parse query parameters
        if 'query' in url:
            for query in url['query']:
                params['query_params'].append({
                    'name': query.get('key', ''),
                    'required': not query.get('disabled', False),
                    'type': 'string'
                })
                
        # Parse headers
        for header in request.get('header', []):
            params['header_params'].append({
                'name': header.get('key', ''),
                'required': True,
                'type': 'string'
            })
            
        # Parse body parameters
        body = request.get('body', {})
        if body.get('mode') == 'raw':
            try:
                body_json = json.loads(body.get('raw', '{}'))
                if isinstance(body_json, dict):
                    for key in body_json.keys():
                        params['body_params'].append({
                            'name': key,
                            'required': True,
                            'type': 'string'
                        })
            except json.JSONDecodeError:
                pass
                
        return params
        
    def _parse_responses(self, item: Dict) -> Dict[str, Any]:
        """Parse response examples from Postman item"""
        responses = {}
        for response in item.get('response', []):
            status = str(response.get('code', ''))
            if status:
                responses[status] = {
                    'description': response.get('name', ''),
                    'content': {
                        'application/json': {
                            'example': response.get('body', '')
                        }
                    }
                }
        return responses
