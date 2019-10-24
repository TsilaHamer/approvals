import logging

DEFAULT_LOGGER_NAME = 'duct_logger'
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_HUMAN_LOG_FORMAT = ('%(process)d - %(asctime)s - %(levelname)s - '
                            '%(name)s - %(module)s - %(funcName)s - '
                            'line %(lineno)d - %(message)s')


def get_logger(logger_name=DEFAULT_LOGGER_NAME, log_level=DEFAULT_LOG_LEVEL,
               enable_machine_log_file=False, enable_human_log_file=False,
               enable_stream_log=True, ignore_log_failures=True,
               machine_log_file_path=None, human_log_file_path=None,
               human_log_format=DEFAULT_HUMAN_LOG_FORMAT, logstash_host=None,
               logstash_port=None, enable_logstash_log=False, **kwargs):
    # IMPORTANT NOTE:
    # depending on environment settings, log failure may be silently ignored.
    # typically, this is done when log failure should not fail the
    # parent process
    try:
        lgr = logging.getLogger(logger_name)
        # adding logger handlers only if no handlers exist.
        # the logger object acts as a singleton by nature,
        # but handlers may be unintentionally duplicated
        if not len(lgr.handlers):
            lgr.setLevel(int(log_level))

            # add stream handler if enabled
            if str(enable_stream_log).lower() == 'true':
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(
                    logging.Formatter(human_log_format))
                lgr.addHandler(stream_handler)


            # add human readable log file handler
            if str(enable_human_log_file).lower() == 'true':
                file_handler = logging.FileHandler(human_log_file_path)
                file_handler.setFormatter(logging.Formatter(human_log_format))
                lgr.addHandler(file_handler)


            # add machine log handler
            if str(enable_machine_log_file).lower() == 'true':
                from logstash_formatter import LogstashFormatter
                file_handler = logging.FileHandler(machine_log_file_path)
                file_handler.setFormatter(LogstashFormatter())
                lgr.addHandler(file_handler)


            # add LogStash handler
            if str(enable_logstash_log).lower() == 'true':
                from logstash import LogstashHandler
                # from logstash_formatter import LogstashFormatter
                logstash_handler = LogstashHandler(
                    logstash_host, int(logstash_port), version=1)
                # logstash_handler.setFormatter(LogstashFormatter())
                lgr.addHandler(logstash_handler)

        return lgr

    except:
        if str(ignore_log_failures).lower() == 'true':
            pass
        else:
            raise
