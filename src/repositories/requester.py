import asyncio
import json
import subprocess


class RequestRepository:
    def __init__(self, timeout: int = 120):
        self.timeout = timeout

    async def get_speedtest_results(self) -> dict:
        try:
            process = await asyncio.create_subprocess_exec(
                "/usr/bin/speedtest-cli",
                "--json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=self.timeout
            )
            return json.loads(stdout.decode())
        except TimeoutError as err:
            raise Exception("Speedtest timed out") from err
        except subprocess.CalledProcessError as e:
            # Now we can access stderr for better error messages
            error_msg = f"Speedtest failed with exit code {e.returncode}"
            if e.stderr:
                error_msg += f": {e.stderr.strip()}"
            raise Exception(error_msg) from e
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse speedtest JSON output: {e}") from e
        except Exception as e:
            raise Exception(f"An error occurred: {e}") from e
