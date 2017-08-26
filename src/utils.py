import logging
import urllib2

logger = logging.getLogger(__name__)


def download_content(url, filename=None):
    """ Download a web page content and decode it.

    :param url: URL of the page.
    :param filename: If defined, page content will be stored there, if not
                     it's returned.
    """
    logger.debug("GET %s", url)
    try:
        resp = urllib2.urlopen(url)
    except (urllib2.HTTPError, urllib2.URLError), e:
        logger.error(e)
        return

    charset = resp.headers.get("charset", "ISO-8859-15")
    content = resp.read().decode(charset).encode("UTF-8")
    if not filename:
        return content

    logger.debug("Writing file %s", filename)
    with open(filename, 'w') as f:
        f.write(content)
