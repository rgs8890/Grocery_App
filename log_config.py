import logging
import os

import constants


# Create the export path if it doesn't exist
os.makedirs(constants.EXPORT_PATH, exist_ok=True)

# Get the log file name
log_file_name = os.path.join(constants.EXPORT_PATH, 'grocery_logger.log')

# Setup the log config
logging.basicConfig(
    filename = log_file_name,
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.StreamHandler()
    ]# Streamhandlers output logs to the console in real time
)

# Log when a function starts or finishes
# Also for the success and failures of processes
# Errors or unexpected behaviour

'''
When commands run,
inputs are received. 
There are also errors which occur.
'''

# Created a log config, and also check to see if the log dir exists. Also set the log file name, Set up the logging.basicConfig
# Added logs to the core module; StreamHandler Setup
# Added logs to the launch module
