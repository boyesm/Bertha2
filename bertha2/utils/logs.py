import logging
from bertha2.settings import cli_args, log_format

def initialize_module_logger(module_name):
    logger = logging.getLogger(module_name)

    # If the debug flag is set high, enable debug level logging
    if "visuals" in module_name and cli_args.debug_visuals:
        logging.getLogger(module_name).setLevel(logging.DEBUG)
    elif "chat" in module_name and cli_args.debug_chat:
        logging.getLogger(module_name).setLevel(logging.DEBUG)
    elif "hardware" in module_name and cli_args.debug_hardware:
        logging.getLogger(module_name).setLevel(logging.DEBUG)
    elif "converter" in module_name and cli_args.debug_converter:
        logging.getLogger(module_name).setLevel(logging.DEBUG)

    return logger


def initialize_root_logger(root_module):
    # This is run before importing B2 modules so that they all have consistent log levels for all code run
    # For more information on log levels: https://docs.python.org/3/library/logging.html#levels
    if cli_args.log is None:  # If LOG isn't defined, set to info mode.
        numeric_level = 20
    else:
        numeric_level = getattr(logging, cli_args.log.upper())
    logging.basicConfig(level=numeric_level, format=log_format)  # NOTE: Without this, logs won't print in the console.
    return logging.getLogger(root_module)


def log_if_in_debug_mode(logger_object, module_name):
    logger_object.debug(f"Debug logging enabled for {module_name}.")
