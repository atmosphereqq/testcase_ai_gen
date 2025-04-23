import pytest
import os
import json
from pathlib import Path
from ..core.parser import SwaggerParser
from ..core.generator import TestCaseGenerator
from ..core.report_generator import ReportGenerator

@pytest.fixture
def order_api_parser():
    test_file = str(Path(__file__).parent.parent / "examples" / "order_api.yaml")
    parser = SwaggerParser(test_file)
    parser.load_spec()
    return parser

def test_normal_case_generation(order_api_parser):
    generator = TestCaseGenerator(order_api_parser)
    cases = generator.generate_normal_cases("/orders", "post")
    
    assert len(cases) == 1
    case = cases[0]
    assert case["type"] == "normal"
    assert case["request"]["method"] == "POST"
    assert "productId" in case["request"]["parameters"]
    assert "quantity" in case["request"]["parameters"]

def test_error_case_generation(order_api_parser):
    generator = TestCaseGenerator(order_api_parser)
    cases = generator.generate_error_cases("/orders", "post")
    
    # Should generate cases for missing productId and quantity
    assert len(cases) == 2  
    for case in cases:
        assert case["type"] == "error"
        assert case["expect"]["status"] == 400

def test_boundary_case_generation(order_api_parser):
    generator = TestCaseGenerator(order_api_parser)
    cases = generator.generate_boundary_cases("/orders", "post")
    
    # Should generate min/max cases for quantity
    assert len(cases) >= 1
    for case in cases:
        assert case["type"] == "boundary"

def test_report_generation(order_api_parser, tmp_path):
    generator = TestCaseGenerator(order_api_parser)
    report_gen = ReportGenerator(str(tmp_path))
    
    # Generate all test cases
    test_cases = []
    test_cases.extend(generator.generate_normal_cases("/orders", "post"))
    test_cases.extend(generator.generate_error_cases("/orders", "post"))
    test_cases.extend(generator.generate_boundary_cases("/orders", "post"))
    
    # Generate and validate report
    report_path = report_gen.generate_json_report(test_cases)
    assert os.path.exists(report_path)
    
    with open(report_path) as f:
        report = json.load(f)
        assert report["metadata"]["total_cases"] == len(test_cases)
        assert report_gen.validate_schema(report["test_cases"])
