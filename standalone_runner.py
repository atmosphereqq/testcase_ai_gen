import sys
import os
import argparse
from pathlib import Path
import yaml
import json
from jinja2 import Environment, FileSystemLoader

from core.parser import SwaggerParser
from core.generator import TestCaseGenerator

class ReportGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

    def generate_json_report(self, test_cases):
        output_file = os.path.join(self.output_dir, 'test_cases.json')
        with open(output_file, 'w') as f:
            json.dump(test_cases, f, indent=2)
        return output_file

    def generate_html_report(self, test_cases):
        template = self.env.get_template('report.html')
        output_file = os.path.join(self.output_dir, 'report.html')
        with open(output_file, 'w') as f:
            f.write(template.render(test_cases=test_cases))
        return output_file

def main():
    parser = argparse.ArgumentParser(description='Swagger Test Case Generator')
    parser.add_argument('swagger_file', help='Path to Swagger/OpenAPI file')
    parser.add_argument('-o', '--output', default='output', help='Output directory')
    args = parser.parse_args()

    # Initialize components
    swagger_parser = SwaggerParser()
    test_generator = TestCaseGenerator(swagger_parser)
    report_generator = ReportGenerator(args.output)

    # Generate test cases for all endpoints
    test_cases = []
    api_def = swagger_parser.parse(args.swagger_file)
    
    for endpoint in api_def.endpoints:
        method = endpoint['method'].lower()
        if method in ['get', 'post', 'put', 'delete', 'patch']:
            path = endpoint['path']
            test_cases.extend(test_generator.generate_normal_cases(path, method))
            test_cases.extend(test_generator.generate_error_cases(path, method))
            test_cases.extend(test_generator.generate_boundary_cases(path, method))

    # Generate reports
    json_report = report_generator.generate_json_report(test_cases)
    html_report = report_generator.generate_html_report(test_cases)
    
    print(f"Generated {len(test_cases)} test cases")
    print(f"JSON report saved to: {json_report}")
    print(f"HTML report saved to: {html_report}")

if __name__ == '__main__':
    main()
