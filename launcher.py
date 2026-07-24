import multiprocessing
import sys
from pathlib import Path

if __name__ == "__main__":
    multiprocessing.freeze_support()

    base_dir = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
    sys.path.insert(0, str(base_dir))

    from streamlit.web import cli

    sys.argv = [
        "streamlit", "run", str(base_dir / "app.py"),
        "--global.developmentMode", "false",
        "--server.port", "8501",
        "--server.address", "127.0.0.1",
        "--browser.gatherUsageStats", "false",
    ]
    cli.main()
