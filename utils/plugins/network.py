import psutil
import logging


class Network:
    def get_network_data(self):
        try:
            psutil.net_io_counters(pernic=True)
            return {
                "addresses": psutil.net_if_addrs(),
                "io": psutil.net_io_counters(pernic=True, nowrap=True),
                "stats": psutil.net_if_stats(),
                "radar_data": [],
            }
        except Exception as e:
            logging.exception(f"cannot get network data: {e}")
            return {
                "error": {
                    "type": "critical",
                    "msg": f"{e}",
                },
            }


if __name__ == "__main__":
    pass
    # network = Network()
    # print(network.get_network_data())
