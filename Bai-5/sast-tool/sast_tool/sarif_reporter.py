import json
from pathlib import Path

class SarifReporter:
    def generate_report(self, issues, output_file='report.sarif', analyzed_file='input.py'):
        uri = Path(analyzed_file).resolve().as_uri()
        levels = {'high': 'error', 'medium': 'warning', 'low': 'note'}
        rules = sorted({issue['type'] for issue in issues})
        results = []
        for issue in issues:
            results.append({'ruleId': issue['type'], 'level': levels.get(issue.get('severity'), 'warning'),
                'message': {'text': issue['message']},
                'locations': [{'physicalLocation': {'artifactLocation': {'uri': uri}, 'region': {
                    'startLine': max(1, issue['lineno']), 'startColumn': max(1, issue['col_offset'] + 1)}}}]})
        log = {'version': '2.1.0', '$schema': 'https://json.schemastore.org/sarif-2.1.0.json',
               'runs': [{'tool': {'driver': {'name': 'PySAST', 'version': '1.0.0',
               'rules': [{'id': r, 'shortDescription': {'text': r}} for r in rules]}}, 'results': results}]}
        Path(output_file).write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding='utf-8')
