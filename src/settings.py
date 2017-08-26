import os

LOG_FILE = "/var/log/aemet/aemet.log"
LOG_FORMAT = (
    '%(asctime)s %(levelname)s %(module)s: %(message)s'
)

DEFAULT_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "aemet_data"
)
