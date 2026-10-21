
import subprocess
import tempfile


class VirtualSandbox:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="lab05_")

    def run_isolated(self, command):
        allowed = {"echo", "printf"}

        if (
            not isinstance(command, list)
            or not command
            or command[0] not in allowed
            or not all(isinstance(arg, str) for arg in command)
        ):
            return "", "Command not permitted in demo sandbox"

        # Mô phỏng các lệnh in văn bản an toàn.
        # Không cần gọi shell của Windows hoặc Linux.
        if command[0] == "echo":
            return " ".join(command[1:]) + "\n", ""

        if command[0] == "printf":
            return "".join(command[1:]), ""

        return "", "Unsupported command"
