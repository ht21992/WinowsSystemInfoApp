import logging
import platform
import multiprocessing
import ctypes
from tools import get_primary_ip
import psutil


class Overview:
    def extract_time_details(self, total_time: int) -> str:
        # extracting hours, minutes, seconds & days from total_time
        # variable (which stores total time in seconds)
        mins, sec = divmod(total_time, 60)
        hour, mins = divmod(mins, 60)
        days, hour = divmod(hour, 24)

        return f"{days} days, {hour:02}:{mins:02}:{sec:02}"

    def _get_load_avg(self):
        "This indicates the number of processes in the system run queue (over the last 1, 5, and 15 minutes)."
        return dict(zip([1, 5, 15], psutil.getloadavg()))

    def _get_cpus(self):
        try:
            # Get the number of CPUs
            cpus = multiprocessing.cpu_count()

            # Get the CPU type/model name
            cpu_type = platform.processor()

            # Sometimes platform.processor() may return an empty string
            # In that case, use psutil to get additional information
            if not cpu_type:
                cpu_type = (
                    psutil.cpu_info().brand_raw
                    if hasattr(psutil, "cpu_info")
                    else "Unknown"
                )

            data = {"cpus": cpus, "type": cpu_type}

        except Exception as err:
            data = str(err)

        return data

    def _get_platform(self) -> dict:
        try:
            uname = platform.uname()
            data = {
                "system": uname[0],
                "hostname": uname[1],
                "release": uname[2],
                "version": uname[3],
                "machine": uname[4],
            }
            return data
        except Exception as e:
            logging.exception(f"cannot get platform data: {e}")
            return {
                "error": {
                    "type": "critical",
                    "msg": f"{e}",
                },
            }

    def _get_uptime(self) -> str:
        try:
            lib = ctypes.windll.kernel32
            t = lib.GetTickCount64()
            # truncating the value since the time is in milliseconds i.e. 1000 * seconds
            total_time = int(str(t)[:-3])
            detailed_up_time = self.extract_time_details(total_time)
            return detailed_up_time
        except Exception as e:
            logging.exception(f"cannot get uptime data: {e}")
            return f"error:{e}"

    def get_overview_data(self):
        try:
            data = {
                "platform": self._get_platform(),
                "uptime": self._get_uptime(),
                "primary_ip": get_primary_ip(),
                "cpus": self._get_cpus(),
            }
            return data
        except Exception as e:
            logging.exception(f"cannot get overview data: {e}")
            return {
                "error": {
                    "type": "critical",
                    "msg": f"{e}",
                },
            }


if __name__ == "__main__":
    pass
    # overview = Overview()
    # print(overview.get_overview_data())
    # print(overview._get_load_avg())
