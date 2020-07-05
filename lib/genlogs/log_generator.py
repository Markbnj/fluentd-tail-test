import logging
import logging.handlers
import pathlib
import time
import os
import random
import string
import fluent.handler


def __get_file_handler(path, id, rotate_max_bytes=5000000, rotate_num_backups=5 ):
  log_name = f"test-log-{id}.log"
  base_path = pathlib.Path(path)
  log_path = base_path / log_name
  handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=rotate_max_bytes, backupCount=rotate_num_backups)
  handler.setFormatter(logging.Formatter('{"time":"%(asctime)s","log":"%(message)s"}'))
  return handler


def __get_fluent_handler(host="localhost", port=24224):
  handler = fluent.handler.FluentHandler('test', host, port)
  formatter = fluent.handler.FluentRecordFormatter({"time":"%(asctime)s","log":"%(message)s"})
  handler.setFormatter(formatter)
  return handler


def generate_logs(run_for_sec, events_per_sec, line_length, id, output_type, path):
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.INFO)
  handler = None

  if output_type == "file":
    handler = __get_file_handler(path, id)
  elif output_type == "push":
    handler = __get_fluent_handler()
  else:
    raise Exception("Unknown output type")

  handler.setLevel(logging.INFO)
  logger.addHandler(handler)

  log_line = "".join(random.choice(string.ascii_lowercase) for i in range(line_length))

  write_delay = 1000000/events_per_sec
  start_s = time.time()
  line_count = 0
  while True:
    logger.log(logging.INFO, log_line)
    line_count = line_count + 1
    if time.time() - start_s > run_for_sec:
      break
    time.sleep(write_delay / 1000000)

  ran_for_sec = time.time() - start_s
  print(f"writer {os.getpid()} exiting; wrote {line_count} lines in {ran_for_sec} seconds.")
