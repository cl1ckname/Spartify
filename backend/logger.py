import logging

api_logger = logging.getLogger('api_logger')
warning_file_handler = logging.FileHandler('logs/api_errors.log')
warning_file_handler.setLevel(logging.WARNING)
warning_formater = logging.Formatter('%(username)s -- %(endpoint)s -- %(status_code)d: %(message)s')
warning_file_handler.setFormatter(warning_formater)
api_logger.addHandler(warning_file_handler)


