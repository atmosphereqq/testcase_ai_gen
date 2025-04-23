import json
import datetime
from typing import Dict, List
from pathlib import Path
import jsonschema
from jinja2 import Template

class ReportGenerator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(exist_ok=True)
        
    def generate_json_report(self, test_cases: List[Dict], filename: str = "test_cases.json") -> str:
        """Generate JSON report from test cases"""
        report = {
            "metadata": {
                "version": "1.0",
                "generated_at": datetime.datetime.now().isoformat(),
                "total_cases": len(test_cases)
            },
            "test_cases": test_cases
        }
        
        output_path = Path(self.output_dir) / filename
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(output_path)
    
    def validate_schema(self, test_cases: List[Dict]) -> bool:
        """Validate test cases against JSON Schema"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "type": {"enum": ["normal", "error", "boundary", "security"]},
                "request": {
                    "type": "object",
                    "properties": {
                        "method": {"type": "string"},
                        "path": {"type": "string"},
                        "parameters": {"type": "object"}
                    },
                    "required": ["method", "path"]
                },
                "expect": {
                    "type": "object",
                    "properties": {
                        "status": {"type": ["number", "array"]},
                        "not_contains": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["status"]
                }
            },
            "required": ["name", "type", "request", "expect"]
        }
        
        for case in test_cases:
            try:
                jsonschema.validate(instance=case, schema=schema)
            except jsonschema.ValidationError:
                return False
        return True

    def generate_html_report(self, test_cases: List[Dict], filename: str = "report.html") -> str:
        """Generate HTML report from test cases"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Case Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                .case { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
                .normal { background-color: #e6f7ff; }
                .error { background-color: #fff2e6; }
                .boundary { background-color: #f6ffed; }
                .security { background-color: #fff0f6; }
            </style>
        </head>
        <body>
            <h1>Test Case Report</h1>
            <p>Generated at: {{ generated_at }}</p>
            <p>Total cases: {{ total_cases }}</p>
            
            {% for case in test_cases %}
            <div class="case {{ case.type }}">
                <h3>{{ case.name }}</h3>
                <p><strong>Type:</strong> {{ case.type }}</p>
                <p><strong>Request:</strong> {{ case.request.method }} {{ case.request.path }}</p>
                <p><strong>Parameters:</strong> {{ case.request.parameters }}</p>
                <p><strong>Expected:</strong> Status {{ case.expect.status }}</p>
            </div>
            {% endfor %}
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            generated_at=datetime.datetime.now().isoformat(),
            total_cases=len(test_cases),
            test_cases=test_cases
        )
        
        output_path = Path(self.output_dir) / filename
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return str(output_path)
