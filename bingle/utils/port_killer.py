import os
import signal
import subprocess
from typing import List


class PortKiller:
    def is_alive(self, port: int) -> bool:
        pid_list = self.search_pid_from(port=port)
        return bool(pid_list)

    def kill(self, port: int):
        pid_list = self.search_pid_from(port=port)
        print(f"Port {port} has been killed.")
        self._kill_processes(pid_list)

    @staticmethod
    def _kill_processes(pid_list: List[int]):
        for pid in pid_list:
            os.kill(pid, signal.SIGILL)
            print(f"(Process {pid} has been killed.)")

    @staticmethod
    def _get_os(in_detail: bool) -> str:
        if in_detail:
            import platform
            # 플랫폼의 상세한 이름을 가져옵니다.
            os_name = platform.platform()
        else:
            # 간략한 운영 체제 이름을 확인합니다.
            if os.name == "nt":
                os_name = "Windows"
            elif os.name == "posix":
                os_name = "Linux/Unix/MacOS"
            else:
                os_name = "Unknown"

        return os_name

    def search_pid_from(self, port: int, status: List[str] = ['established', 'listening']) -> List[int]:
        # 해당 포트를 사용하는 프로세스의 PID를 찾는 명령어입니다.
        # netstat은 네트워크 상태를, grep은 문자열을 검색합니다.
        osname_lower = self._get_os(in_detail=False).lower()
        if "windows" in osname_lower:
            command = f"netstat -ano | findstr :{port}"
        elif "linux" in osname_lower:
            command = f"netstat -nlp | grep :{port}"
        else:
            raise NotImplementedError()

        # 명령어를 실행하여 결과를 받아옵니다.
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        # 결과에서 PID를 추출합니다.
        pid_list = list()
        for line in out.splitlines():
            condition = f":{port}" in str(line)
            condition = condition and any([st in str(line).lower() for st in status])
            if condition:
                pid = int(line.decode().split()[-1].split('/')[0])
                if pid not in pid_list:
                    pid_list.append(pid)

        return pid_list
