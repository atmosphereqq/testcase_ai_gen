import argparse
from pathlib import Path
from swagger_testgen.core.parser import SwaggerParser
from swagger_testgen.core.postman_parser import PostmanParser
from swagger_testgen.core.generator import TestCaseGenerator
from swagger_testgen.core.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description='Swagger Test Case Generator')
    parser.add_argument('swagger_file', help='Path to Swagger/OpenAPI file')
    parser.add_argument('-o', '--output', default='output', help='Output directory')
    args = parser.parse_args()

    # Initialize appropriate parser
    if args.swagger_file.endswith('.json'):
        parser = PostmanParser()
    else:
        parser = SwaggerParser()
    
    test_generator = TestCaseGenerator(parser)
    report_generator = ReportGenerator(args.output)

    # Generate test cases for all endpoints
    test_cases = []
    api_def = parser.parse(args.swagger_file)
    
    for endpoint in api_def.endpoints:
        method = endpoint['method'].lower()
        if method in ['get', 'post', 'put', 'delete', 'patch']:
            path = endpoint['path']
            test_cases.extend(test_generator.generate_normal_cases(path, method))
            test_cases.extend(test_generator.generate_error_cases(path, method))
            test_cases.extend(test_generator.generate_boundary_cases(path, method))
            test_cases.extend(test_generator.generate_security_cases(path, method))

    # Generate reports
    json_report = report_generator.generate_json_report(test_cases)
    html_report = report_generator.generate_html_report(test_cases)
    
    print(f"Generated {len(test_cases)} test cases")
    print(f"JSON report saved to: {json_report}")
    print(f"HTML report saved to: {html_report}")

if __name__ == '__main__':
    main()
