#!/usr/bin/env python

import argparse
import logging
import os
import sys
import time

import parsers
import settings
from src import utils

logger = logging.getLogger(__name__)

MAIN_URL = "http://www.aemet.es/es/eltiempo/observacion/ultimosdatos"
STATE_URL = MAIN_URL + "?k=%s&w=0&datos=det&x=h24&f=temperatura"
STATION_URL = MAIN_URL + "_%s_datos-horarios.csv?k=%s&l=%s&datos=det"


def download_data(output, c_time, format):
    main_content = utils.download_content(MAIN_URL)
    state_parser = parsers.MainParser(main_content)
    for state in state_parser.get_match():
        logger.debug("Processing state %s", state)
        download_state_data(state, output, c_time, format)


def download_state_data(state, output, c_time, format):
    state_content = utils.download_content(STATE_URL % state)
    state_parser = parsers.StateParser(state_content)
    for station in state_parser.get_match():
        logger.debug("Processing station %s", station)
        download_station_data(state, station, output, c_time)


def download_station_data(state, station, output, c_time):
    def _get_station_filename():
        """ Returns the full path where to download the file creating the
        necessary directories. """
        output_dir = os.path.join(output, state, station)
        if not os.path.isdir(output_dir):
            logger.debug("Creating directory %s", output_dir)
            os.makedirs(output_dir)
        return os.path.join(output_dir, "%s.%s" % (c_time, format))

    url = STATION_URL % (station, state, station)
    filename = _get_station_filename()
    utils.download_content(url, filename)


def parse_options():
    parser = argparse.ArgumentParser(
        description=("Download the hourly weather data for all the"
                     " stations available in aemet.es.")
    )
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Enable debug mode.")
    parser.add_argument('-v', '--verbose', default="2",
                        help="Verbosity level. Options: 0=ERROR,"
                                 " 1=WARNING, 2=INFO or 3=DEBUG. Default: 2.")
    parser.add_argument('-o', '--output',
                        default=settings.DEFAULT_OUTPUT_DIR,
                        help="Output directory path where files will be"
                             " downloaded. Default: aemet_data.")
    parser.add_argument('-f', '--format', default='txt',
                        help="Store file in the specified format."
                             "Options: csv or txt. Default: csv.")
    return parser.parse_args()


def main(options):
    logger.debug("Storing files into %s", options.output)
    if not os.path.isdir(options.output):
        os.mkdir(options.output)
    download_data(
        output=options.output,
        c_time=time.strftime("%Y%m%d%H00"),
        format=options.format
    )


def get_logger_config(options):
    logging_options = dict(level=logging.DEBUG, format=settings.LOG_FORMAT)
    if options.debug:
        return logging_options

    if options.verbose == "0":
        logging_options['level'] = logging.ERROR
    elif options.verbose == "1":
        logging_options['level'] = logging.WARNING
    elif options.verbose == "2":
        logging_options['level'] = logging.INFO

    log_basedir = os.path.dirname(settings.LOG_FILE)
    if not os.path.exists(log_basedir):
        os.makedirs(log_basedir)
    log_file = settings.LOG_FILE % time.strftime('%Y%m%d')
    logging_options['filename'] = log_file
    return logging_options


if __name__ == '__main__':
    opts = parse_options()
    logging.basicConfig(**get_logger_config(opts))

    logger.info("Start")
    try:
        main(opts)
    except Exception:
        logger.exception("Unknown error when getting AEMET data.")
        sys.exit(1)

    logger.info("Done")

    sys.exit(0)
