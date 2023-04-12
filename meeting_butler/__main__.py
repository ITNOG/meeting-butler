"""
Main entrypoint for the package.
"""

import logging
from time import sleep

from meeting_butler.meeting_butler import sync
from meeting_butler.settings import Settings


def __main__() -> None:
    """
    Main application entrypoint.
    Stats an infiite loop executing sync() every `sync_every` seconds
    """
    settings = Settings()

    logging.basicConfig()
    logger = logging.getLogger("meeting_butler")

    if settings.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debugging is ON")
    else:
        logger.setLevel(logging.INFO)

    while True:
        sync(
            settings.eventbrite_event,
            settings.eventbrite_token,
            settings.meetingtool_hostname,
            settings.meetingtool_token,
            settings.cache_filename,
        )

        sleep(settings.sync_every)


if __name__ == "__main__":
    __main__()
