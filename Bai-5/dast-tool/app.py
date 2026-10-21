from flask import Flask, jsonify, request
import os
from runtime_monitor import RuntimeMonitor
from memory_analyzer import MemoryAnalyzer
from network_traffic_analyzer import NetworkTrafficAnalyzer
from security_behavior_checker import SecurityBehaviorChecker
from virtual_sandbox import VirtualSandbox

app = Flask(__name__)
pid = os.getpid()

@app.route('/api/monitor', methods=['GET'])
def monitor():
    rm = RuntimeMonitor(pid)
    return jsonify({'cpu_usage': rm.get_cpu_usage(), 'memory_usage': rm.get_memory_usage(), 'open_files': [p.path for p in rm.get_open_files()]})

@app.route('/api/memory', methods=['GET'])
def memory():
    ma = MemoryAnalyzer()
    return jsonify({'memory_leaks': len(ma.check_memory_leaks()), 'overflow_test': ma.check_overflow(2**64)})

@app.route('/api/network', methods=['GET'])
def network():
    return jsonify({'network_stats': {k: v._asdict() for k, v in NetworkTrafficAnalyzer().get_network_stats().items()}})

@app.route('/api/security', methods=['GET'])
def security():
    return jsonify({'suspicious_calls': SecurityBehaviorChecker().suspicious_calls()})

@app.route('/api/sandbox', methods=['POST'])
def sandbox():
    data = request.get_json(silent=True) or {}
    command = data.get('command')
    if not isinstance(command, list):
        return jsonify({'error': 'command must be a list, e.g. ["echo", "hello"]'}), 400
    stdout, stderr = VirtualSandbox().run_isolated(command)
    return jsonify({'stdout': stdout, 'stderr': stderr})

@app.route("/")
def home():
    return {
        "application": "LAB 05 - DAST Tool",
        "status": "running",
        "endpoints": [
            "/api/monitor",
            "/api/memory",
            "/api/network",
            "/api/security",
            "/api/sandbox"
        ]
    }

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
