import psutil
import logging


class Disk:


    def resolve_partition(self, partition):
        # On Windows, partitions are like 'C:\\', 'D:\\', so we just take the drive letter
        device = partition.device
        device = device.rstrip("\\")  # Strip trailing backslash for easier comparison
        return device

    def get_disk_io_data(self):
        partitions = psutil.disk_partitions(all=False)
        diskrw = psutil.disk_io_counters(perdisk=True)

        diskrw_data = {
            "read_bytes": 0,
            "write_bytes": 0,
        }

        # List of partitions' drive letters in Windows (e.g., 'C:', 'D:')
        io_disks = [
            self.resolve_partition(p)
            for p in partitions
            if p.fstype != ""  # Skip CD-ROMs
        ]

        matched_disks = {k: v for k, v in diskrw.items() if k in io_disks}

        if not matched_disks:
            # Try fallback for other device names (e.g., 'PhysicalDrive0')
            matched_disks = diskrw

        for k, io in matched_disks.items():
            diskrw_data["read_bytes"] += io.read_bytes
            diskrw_data["write_bytes"] += io.write_bytes

        return {"io": matched_disks, "total_io": diskrw_data}

    def get_disk_data(self):
        try:
            partitions = psutil.disk_partitions(all=False)
            disk_data = {}

            for partition in partitions:
                if "loop" in partition.device:
                    continue  # ignore it
                current_disk_usage = psutil.disk_usage(partition.mountpoint)
                disk_data[partition.mountpoint] = current_disk_usage

            return disk_data

        except Exception as e:
            logging.exception(f"cannot get disk data: {e}")
            return {
                "error": {
                    "type": "critical",
                    "msg": f"{e}",
                },
            }


if __name__ == "__main__":
    pass
    # disk = Disk()
    # print(disk.get_disk_data())
    # print(disk.get_disk_io_data())
