import logging

from bertha2.settings import cli_args

# Easily create ANSI escape codes here: https://ansi.gabebanks.net
MAGENTA = "\x1b[35;49;1m"
BLUE = "\x1b[34;49;1m"
GREEN = "\x1b[32;49;1m"
RESET = "\x1b[0m"
# This format is aligned for ease of reading
log_formatter = logging.Formatter(f"{BLUE}[%(levelname)-10s]{MAGENTA}[%(name)-20s]{RESET} %(message)-75s     {GREEN}[%(filename)s:%(lineno)d]{RESET}")
# log_format = f"{blue}[%(levelname)s]{magenta}[%(name)s]{reset} %(message)s     {green}[%(filename)s:%(lineno)d]{reset}"

def get_module_logger(module_name):
    """
    Gets the logger with the correct logging level for a specific module
    For more information on log levels: https://docs.python.org/3/library/logging.html#levels
    :param module_name: This should be the name of the module that calls this function
    :return: The logger for the current module with the correct settings
    """
    logging_level = cli_args.log_level
    # Find our current logger and check if any flags are set for it
    if "main" in module_name:
        if cli_args.log_level_main:
            logging_level = cli_args.log_level_main
    elif "visuals" in module_name:
        if cli_args.log_level_visuals:
            logging_level = cli_args.log_level_visuals
    elif "chat" in module_name:
        if cli_args.log_level_chat:
            logging_level = cli_args.log_level_chat
    elif "hardware" in module_name:
        if cli_args.log_level_hardware:
            logging_level = cli_args.log_level_hardware
    elif "converter" in module_name:
        if cli_args.log_level_converter:
            logging_level = cli_args.log_level_converter
    else:
        print(f"UNKNOWN MODULE: {module_name}. Returning generic logger")
        return logging.getLogger('B2')
    logging_level = int(logging_level)
    # print(f"Logging level for: {module_name}: {logging_level}")

    logger = logging.getLogger(module_name)

    if cli_args.log_to_file:
        # Add handler so we can print to a file
        file_handler = logging.FileHandler("./B2-logs.txt")
        file_handler.setFormatter(log_formatter)
        logger.addHandler(file_handler)

    # Add handler so we can print to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging_level)


    return logger
