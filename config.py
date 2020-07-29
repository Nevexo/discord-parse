# Configuration values used by parser

import os

# Location of discord export
EXPORT_DIR = os.path.join(os.getcwd(), "export")

# === MESSAGES ===

# You must have sent a message within the past N to mark a guild as active.
# This is a little inaccurate as the time of export likely don't align with
# your system time.
IS_ACTIVE_DAYS = 7
