import sys
from pathlib import Path
from .ast_analyzer import ASTAnalyzer
from .vuln_pattern_matcher import VulnPatternMatcher
from .security_rule_engine import SecurityRuleEngine
from .code_quality_checker import CodeQualityChecker
from .sarif_reporter import SarifReporter

def main(file_path):
    code = Path(file_path).read_text(encoding='utf-8')
    ast_issues = ASTAnalyzer().analyze(code)
    pattern_issues = VulnPatternMatcher().match(code)
    quality_issues = CodeQualityChecker().check(file_path)
    issues = SecurityRuleEngine().evaluate(ast_issues, pattern_issues) + quality_issues
    SarifReporter().generate_report(issues, analyzed_file=file_path)
    print(f'Analysis complete. Report saved to report.sarif with {len(issues)} issues.')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python -m sast_tool.main <file_to_analyze.py>')
        sys.exit(1)
    main(sys.argv[1])
