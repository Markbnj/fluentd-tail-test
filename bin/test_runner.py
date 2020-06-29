from argparse import ArgumentParser
from pathlib import Path
import logging
import logging.handlers
import time
from multiprocessing import Process
import os


def write_logs(run_for, events_per_sec, id, output_type, path):
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  handler = None

  if output_type == 'file':
    log_name = f"test-log-{id}.log"
    base_path = Path(path)
    log_path = base_path / log_name
    handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=5000000, backupCount=5)
  elif output_type == 'push':
    raise Exception("Not implemented")
  else:
    raise Exception("Unknown output type")

  handler.setFormatter(logging.Formatter('{"time":"%(asctime)s","log":"%(message)s"}'))
  logger.addHandler(handler)

  write_delay = 1000000/events_per_sec
  start_s = time.time()
  line_count = 0
  while True:
    logger.debug('This is a test log line; no actual event has occurred')
    line_count = line_count + 1
    if time.time() - start_s > run_for:
      break
    time.sleep(write_delay / 1000000)

  ran_for = time.time() - start_s
  print(f'writer {os.getpid()} exiting; wrote {line_count} lines in {ran_for} seconds.')


def run_test(num_writers, run_for, events_per_sec, output_type, path):
  procs = []
  for i in range(num_writers):
    p = Process(target=write_logs, args=(run_for,events_per_sec,i,output_type,path))
    p.start()
    procs.append(p)
  while [p.exitcode for p in procs if p.exitcode is None]:
    time.sleep(2)


if __name__ == "__main__":
  parser = ArgumentParser(description='Run a log write test using multiple writers')
  parser.add_argument('-n', '--num-writers', type=int, required=True, help='The number of log writers to spawn.')
  parser.add_argument('-r', '--run-for', type=int, required=True, help='Running time of the test in seconds.')
  parser.add_argument('-e', '--events-per-sec', type=int, required=True, help='Number of events to emit per second.')
  parser.add_argument('-o', '--output-type', required=True, help='Kind of log output file|push')
  parser.add_argument('-p', '--path', default='srclogs', help='Path where logs are written.')

  args = parser.parse_args()
  print(f'spawning log writers with args: {args}')
  run_test(args.num_writers, args.run_for, args.events_per_sec, args.output_type, args.path )
