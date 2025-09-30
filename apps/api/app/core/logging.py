import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    # Uvicorn already configures loggers; we align formats and levels.
    fmt = "%(levelname)s %(asctime)s %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    root = logging.getLogger()
    root.setLevel(level)

    # Clear existing handlers if any (avoid duplicates on reload)
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    root.addHandler(handler)

    # Make SQLAlchemy chattier only when debugging
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)