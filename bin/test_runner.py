from argparse import ArgumentParser
from pathlib import Path
import logging
import time
from multiprocessing import Process


def write_logs(run_for, write_delay, id, output_type, path):
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  handler = None

  if output_type == 'file':
    log_name = f"test-log-{id}.log"
    base_path = Path(path)
    log_path = base_path / log_name
    handler = logging.FileHandler(log_path)
  elif output_type == 'network':
    raise Exception("Not implemented")
  else:
    raise Exception("Unknown output type")

  handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
  logger.addHandler(handler)

  start_s = time.time()
  while True:
    logger.debug('This is a test log line; no actual event has occurred')
    if time.time() - start_s > run_for:
      break
    time.sleep(write_delay / 1000000)


def run_test(num_writers, run_for, write_delay, output_type, path):
  for i in range(num_writers):
    p = Process(target=write_logs, args=(run_for,write_delay,i,output_type,path))
    p.start()
    p.join()


if __name__ == "__main__":
  parser = ArgumentParser(description='Run a log write test using multiple writers')
  parser.add_argument('-n', '--num-writers', type=int, required=True, help='The number of log writers to spawn.')
  parser.add_argument('-r', '--run-for', type=int, required=True, help='Running time of the test in seconds.')
  parser.add_argument('-w', '--write-delay', type=int, required=True, help='Delay between writes in microseconds.')
  parser.add_argument('-o', '--output-type', required=True, help='Kind of log output file|network')
  parser.add_argument('-p', '--path', default='srclogs', help='Path where logs are written.')

  args = parser.parse_args()
  print(args)
  run_test(args.num_writers, args.run_for, args.write_delay, args.output_type, args.path )
