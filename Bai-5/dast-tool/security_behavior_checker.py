from pathlib import Path

class SecurityBehaviorChecker:
    def suspicious_calls(self):
        suspicious = []
        calls = ['os.system', 'eval', 'exec']
        try:
            content = Path(__file__).read_text(encoding='utf-8')
            for call in calls:
                if call in content:
                    suspicious.append(call)
        except OSError:
            pass
        return suspicious
