import psutil
import logging
from datetime import datetime


class User:
    def get_users(self):
        errors = []
        users = []
        try:
            users_info = psutil.users()
            for i, user in enumerate(users_info):
                d = user._asdict()
                d["started"] = datetime.fromtimestamp(d["started"])

                # Get the process details if the PID exists
                try:
                    process = psutil.Process(d["pid"])
                    d["process_name"] = process.name()
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    d["process_name"] = "Unknown"

                users.append(d)
        except Exception as e:
            logging.exception("Cannot get psutil user data")
            errors.append(
                {"type": "critical", "message": f"user psutil exception: {str(e)}"}
            )

        return {"logged_in": users, "errors": errors}


if __name__ == "__main__":
    pass
    # handler = User()
    # user_data = handler.get_users()
    # print(user_data)
