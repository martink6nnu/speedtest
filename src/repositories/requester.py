import subprocess
import json
class RequestRepository:
    def __init__(self, timeout: int = 120):
        self.timeout = timeout
        
    def get_speedtest_results(self) -> dict:
        try:
            result = subprocess.run(["speedtest-cli", "--json"], timeout=self.timeout)
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            raise Exception("Speedtest timed out")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Speedtest failed: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
        
