import logging

# Set up a logger
logger = logging.getLogger(__name__)

# Set the logging level. This can be changed to DEBUG, ERROR, etc. as per your need.
logger.setLevel(logging.INFO)

# Define a Handler that writes log messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# # Define a Handler that writes log messages to a file, with a certain log level
# file_handler = logging.FileHandler('app.log', mode='a')  # 'a' means append mode, 'w' would overwrite the file
# file_handler.setLevel(logging.INFO)

# Create a Formatter for our log messages. This can be customized as needed.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the Formatter for our Handlers
console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)

# Add the Handlers to our Logger
logger.addHandler(console_handler)
# logger.addHandler(file_handler)