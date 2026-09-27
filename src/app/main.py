"""Entry point. Replace with the project's real code."""

import logging
import os

log = logging.getLogger("app")


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    log.info("app started (env=%s)", os.getenv("APP_ENV", "dev"))


if __name__ == "__main__":
    main()
