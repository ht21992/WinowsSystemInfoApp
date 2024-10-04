import psutil
import logging



class CPU:
    def get_cpu_data(self, **params):
        try:
            data = {
                "cpu_percent": psutil.cpu_percent(interval=1, percpu=True),
                "cpu_frequency": [i._asdict() for i in psutil.cpu_freq(percpu=True)],
                "memory": psutil.virtual_memory()._asdict(),
                "swap": psutil.swap_memory()._asdict(),
            }
        except Exception as e:
            logging.exception(f"cannot get cpu data: {e}")
            data = {
                "cpu_percent": [],
                "cpu_frequency": [],
                "cpu_temp": "",
                "memory": {},
                "swap": {},
                "error": {
                    "type": "critical",
                    "msg": f"{e}",
                },
            }

        return data


if __name__ == "__main__":
    pass
    # cpu = CPU()
    # print(cpu.get_cpu_data())
