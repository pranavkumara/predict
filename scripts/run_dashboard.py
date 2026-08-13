"""Start the Streamlit dashboard."""

import subprocess
import sys

from config.settings import settings


def main():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "dashboard/app.py",
            "--server.port",
            str(settings.dashboard_port),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
