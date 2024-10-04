import subprocess


class Power:
    def __abort_shut_down_sys(self):
        subprocess.call(["shutdown", "/a "])

    def __shut_down_sys(self):
        "Shutting down the sys after 60 seconds"
        subprocess.call(["shutdown", "/s", "/t", "60"])

    def __restart_sys(self):
        "Restarting the sys after 60 seconds"
        subprocess.call(["shutdown", "/r", "/t", "60"])

    def __logout_sys(self):
        subprocess.call(["shutdown", "/l"])


if __name__ == "__main__":
    pass
    # power = Power()
    # power.__shut_down_sys()
    # power.__abort_shut_down_sys()
