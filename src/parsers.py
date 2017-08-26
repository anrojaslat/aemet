import logging
import os
import re

import utils

logger = logging.getLogger(__name__)

STATE_REGEX = re.compile(r"k=(\w\w\w)&amp;w=0\">")
STATION_REGEX = re.compile(r"<option value=\"(\d\d\d\d\w?)\">")


class ParseError(Exception):
    pass


class BaseParser(object):
    """ Parser class to, given a regex, get all the matches in the content """
    def __init__(self, content=None):
        self.content = content

    def get_match(self):
        """ Gets all the regex matches in a string. """
        if not self.regex:
            raise Exception("Missing regex")

        if not self.content:
            raise ParseError("Missing content")

        for m in re.finditer(self.regex, self.content):
            if m:
                yield m.group(1)


class MainParser(BaseParser):
    regex = STATE_REGEX


class StateParser(BaseParser):
    regex = STATION_REGEX
