"""
Main entrypoint for the package.
"""

import argparse
import logging
import sys
from time import sleep

from pydantic import ValidationError

from meeting_butler.meeting_butler import sync
from meeting_butler.settings import Settings


def main() -> None:
    """
    Main application entrypoint.
    Stats an infiite loop executing sync() every `sync_every` seconds
    """
    try:
        settings = Settings()
    except ValidationError as error:
        sys.exit(error)

    logging.basicConfig()
    logger = logging.getLogger("meeting_butler")

    if settings.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debugging is ON")
    else:
        logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(
        prog="meeting_butler",
        description="Takes care of background tasks pertained to meeting and registrations",
    )
    parser.add_argument(
        "email_regex",
        metavar="REGEX",
        nargs="?",
        type=str,
        help="Only process attendees whos email address matches with this regex",
        default=False,
    )
    args = parser.parse_args()

    source_settings = {}
    if settings.data_source == "eventbrite":
        source_settings = {"token": settings.eventbrite_token, "event": settings.eventbrite_event}
    elif settings.data_source == "formbuilder":
        source_settings = {"url": settings.formbuilder_url}

    while True:
        sync(
            settings.meetingtool_hostname,
            settings.meetingtool_token,
            source_settings,
            settings.data_source,
            settings.cache_filename,
            args.email_regex,
        )

        sleep(int(settings.sync_every))


if __name__ == "__main__":
    main()
