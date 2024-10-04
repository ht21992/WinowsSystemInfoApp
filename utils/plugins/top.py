import psutil


class Top:
    def _get_process_list_pid(self):
        return psutil.pids()

    def inspect_process(self, pid: int):
        process = psutil.Process(pid)
        return process

    def _list_processes(self):
        proc_list = []
        for proc in psutil.process_iter():
            try:
                ps_info = proc.as_dict()
                # Virtual Memory System
                ps_info["vms"] = proc.memory_info().vms / (1024 * 1024)
                proc_list.append(ps_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return proc_list


if __name__ == "__main__":
    pass
    # top = Top()
    # print(top._list_processes())
    # print(top._get_process_list_pid())
    # print(psutil.Process(24568))
