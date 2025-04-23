from typing import Dict, List, Any
from core.parsers.iapi_parser import IApiParser, ApiDefinition

class TestCaseGenerator:
    def __init__(self, parser: IApiParser):
        self.parser = parser
        
    def _get_parameters_from_endpoint(self, endpoint: Dict) -> Dict[str, Any]:
        """Extract parameters from endpoint definition"""
        params = endpoint.get('parameters', {})
        return {
            'path_params': [p for p in params.get('path_params', [])],
            'query_params': [p for p in params.get('query_params', [])],
            'header_params': [p for p in params.get('header_params', [])],
            'body_params': [p for p in params.get('body_params', [])]
        }

    def generate_normal_cases(self, path: str, method: str) -> List[Dict[str, Any]]:
        """Generate normal flow test cases"""
        cases = []
        # Use the original file path stored in parser
        api_def = self.parser.api_def
        endpoint = next((e for e in api_def.endpoints 
                       if e['path'] == path and e['method'] == method.upper()), None)
        if not endpoint:
            return cases
            
        params = self._get_parameters_from_endpoint(endpoint)
        
        # Generate case with all required parameters
        case = {
            'name': f"{method.upper()}_{path.replace('/', '_')}_normal",
            'type': 'normal',
            'request': {
                'method': method.upper(),
                'path': path,
                'parameters': {}
            },
            'expect': {
                'status': 200
            }
        }
        
        # Add required parameters
        for param_type, param_list in params.items():
            for param in param_list:
                if param.get('required', False):
                    case['request']['parameters'][param['name']] = self._get_sample_value(param)
        
        cases.append(case)
        return cases
    
    def generate_error_cases(self, path: str, method: str) -> List[Dict[str, Any]]:
        """Generate error flow test cases"""
        cases = []
        api_def = self.parser.api_def
        endpoint = next((e for e in api_def.endpoints 
                       if e['path'] == path and e['method'] == method.upper()), None)
        if not endpoint:
            return cases
            
        params = self._get_parameters_from_endpoint(endpoint)
        
        # Case 1: Missing required parameter
        for param_type, param_list in params.items():
            for param in param_list:
                if param.get('required', False):
                    case = {
                        'name': f"{method.upper()}_{path.replace('/', '_')}_missing_{param['name']}",
                        'type': 'error',
                        'request': {
                            'method': method.upper(),
                            'path': path,
                            'parameters': {}
                        },
                        'expect': {
                            'status': 400
                        }
                    }
                    # Add other required params except the missing one
                    for other_param in [p for p in param_list if p.get('required', False) and p['name'] != param['name']]:
                        case['request']['parameters'][other_param['name']] = self._get_sample_value(other_param)
                    
                    cases.append(case)
        
        return cases
    
    def _get_sample_value(self, param: Dict[str, Any]) -> Any:
        """Generate sample value based on parameter definition"""
        if 'example' in param:
            return param['example']
        
        param_type = param.get('type', 'string')
        if param_type == 'integer':
            return 123
        elif param_type == 'boolean':
            return True
        elif param_type == 'number':
            return 1.23
        else:  # string
            return "sample_value"

    def generate_boundary_cases(self, path: str, method: str) -> List[Dict[str, Any]]:
        """Generate boundary value test cases"""
        cases = []
        api_def = self.parser.api_def
        endpoint = next((e for e in api_def.endpoints 
                       if e['path'] == path and e['method'] == method.upper()), None)
        if not endpoint:
            return cases
            
        params = self._get_parameters_from_endpoint(endpoint)
        
        for param_type, param_list in params.items():
            for param in param_list:
                param_type = param.get('type', 'string')
                
                # Numeric boundary cases
                if param_type in ['integer', 'number']:
                    # Zero value case
                    case = {
                        'name': f"{method.upper()}_{path.replace('/', '_')}_zero_{param['name']}",
                        'type': 'boundary',
                        'request': {
                            'method': method.upper(),
                            'path': path,
                            'parameters': {}
                        },
                        'expect': {'status': 200}
                    }
                    # Add all required params
                    for p in [p for p in param_list if p.get('required', False)]:
                        if p['name'] == param['name']:
                            value = 0
                        else:
                            value = self._get_sample_value(p)
                        case['request']['parameters'][p['name']] = value
                    cases.append(case)

                    # Min boundary case
                    if 'minimum' in param:
                        case = {
                            'name': f"{method.upper()}_{path.replace('/', '_')}_min_{param['name']}",
                            'type': 'boundary',
                            'request': {
                                'method': method.upper(),
                                'path': path,
                                'parameters': {}
                            },
                            'expect': {'status': 200}
                        }
                        # Add all required params
                        for p in [p for p in param_list if p.get('required', False)]:
                            if p['name'] == param['name']:
                                value = param['minimum']
                            else:
                                value = self._get_sample_value(p)
                            case['request']['parameters'][p['name']] = value
                        cases.append(case)

                    # Max boundary case
                    if 'maximum' in param:
                        case = {
                            'name': f"{method.upper()}_{path.replace('/', '_')}_max_{param['name']}",
                            'type': 'boundary',
                            'request': {
                                'method': method.upper(),
                                'path': path,
                                'parameters': {}
                            },
                            'expect': {'status': 200}
                        }
                        # Add all required params
                        for p in [p for p in param_list if p.get('required', False)]:
                            if p['name'] == param['name']:
                                value = param['maximum']
                            else:
                                value = self._get_sample_value(p)
                            case['request']['parameters'][p['name']] = value
                        cases.append(case)

                # String boundary cases
                elif param_type == 'string':
                    # Enum invalid value case
                    if param.get('enum'):
                        case = {
                            'name': f"{method.upper()}_{path.replace('/', '_')}_invalid_enum_{param['name']}",
                            'type': 'boundary',
                            'request': {
                                'method': method.upper(),
                                'path': path,
                                'parameters': {}
                            },
                            'expect': {'status': 400}
                        }
                        # Add all required params
                        for p in [p for p in param_list if p.get('required', False)]:
                            if p['name'] == param['name']:
                                value = "INVALID_" + param['enum'][0]  # Generate invalid enum value
                            else:
                                value = self._get_sample_value(p)
                            case['request']['parameters'][p['name']] = value
                        cases.append(case)

                    # Min length case
                    if param.get('minLength') is not None:
                        case = {
                            'name': f"{method.upper()}_{path.replace('/', '_')}_min_length_{param['name']}",
                            'type': 'boundary',
                            'request': {
                                'method': method.upper(),
                                'path': path,
                                'parameters': {}
                            },
                            'expect': {'status': 200}
                        }
                        # Add all required params
                        for p in [p for p in param_list if p.get('required', False)]:
                            if p['name'] == param['name']:
                                value = "a" * param['minLength']
                            else:
                                value = self._get_sample_value(p)
                            case['request']['parameters'][p['name']] = value
                        cases.append(case)

                    # Max length case
                    if param.get('maxLength') is not None:
                        case = {
                            'name': f"{method.upper()}_{path.replace('/', '_')}_max_length_{param['name']}",
                            'type': 'boundary',
                            'request': {
                                'method': method.upper(),
                                'path': path,
                                'parameters': {}
                            },
                            'expect': {'status': 200}
                        }
                        # Add all required params
                        for p in [p for p in param_list if p.get('required', False)]:
                            if p['name'] == param['name']:
                                value = "a" * param['maxLength']
                            else:
                                value = self._get_sample_value(p)
                            case['request']['parameters'][p['name']] = value
                        cases.append(case)
        
        return cases

    def generate_security_cases(self, path: str, method: str) -> List[Dict[str, Any]]:
        """Generate security test cases based on OWASP Top 10"""
        cases = []
        api_def = self.parser.api_def
        endpoint = next((e for e in api_def.endpoints 
                       if e['path'] == path and e['method'] == method.upper()), None)
        if not endpoint:
            return cases
            
        params = self._get_parameters_from_endpoint(endpoint)
        
        # SQL Injection test cases
        for param_type, param_list in params.items():
            for param in param_list:
                if param.get('type') == 'string':
                    case = {
                        'name': f"{method.upper()}_{path.replace('/', '_')}_sqli_{param['name']}",
                        'type': 'security',
                        'request': {
                            'method': method.upper(),
                            'path': path,
                            'parameters': {}
                        },
                        'expect': {
                            'status': [400, 401, 403, 500],  # Any of these would indicate proper handling
                            'not_contains': ['SQL syntax', 'error in your SQL']
                        }
                    }
                    # Add all parameters with attack vector in the target param
                    for p in param_list:
                        if p.get('required', False):
                            if p['name'] == param['name']:
                                case['request']['parameters'][p['name']] = "admin' OR '1'='1"
                            else:
                                case['request']['parameters'][p['name']] = self._get_sample_value(p)
                    cases.append(case)
        
        return cases
