import argparse
from pathlib import Path
from swagger_testgen.core.parser import SwaggerParser
from swagger_testgen.core.generator import TestCaseGenerator
from swagger_testgen.core.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description='Swagger Test Case Generator')
    parser.add_argument('swagger_file', help='Path to Swagger/OpenAPI file')
    parser.add_argument('-o', '--output', default='output', help='Output directory')
    args = parser.parse_args()

    # Initialize components
    swagger_parser = SwaggerParser(args.swagger_file)
    swagger_parser.load_spec()
    
    test_generator = TestCaseGenerator(swagger_parser)
    report_generator = ReportGenerator(args.output)

    # Generate test cases for all paths
    test_cases = []
    paths = swagger_parser.parse_paths()
    
    for path, methods in paths.items():
        for method in methods:
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
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
