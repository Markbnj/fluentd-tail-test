import argparse
import multiprocessing
import time
from genlogs import generate_logs


def run_test(num_writers, run_for_sec, events_per_sec, line_length, output_type, log_path, fluent_server, fluent_port):
  procs = []
  for i in range(num_writers):
    p = multiprocessing.Process(
      target=generate_logs,
      args=(run_for_sec,events_per_sec,line_length,i,output_type,log_path,fluent_server,fluent_port)
    )
    p.start()
    procs.append(p)
  while [p.exitcode for p in procs if p.exitcode is None]:
    time.sleep(5)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Run a log write test using multiple writers')
  parser.add_argument('-n', '--num-writers', type=int, required=True, help='The number of log writers to spawn.')
  parser.add_argument('-r', '--run-for-sec', type=int, required=True, help='Running time of the test in seconds.')
  parser.add_argument('-e', '--events-per-sec', type=int, required=True, help='Number of events to emit per second.')
  parser.add_argument('-l', '--line-length', type=int, required=True, help='Length of the test log lines.')
  parser.add_argument('-o', '--output-type', required=True, help='Kind of log output file|push')
  parser.add_argument('-f', '--log-path', default='srclogs', help='Path where logs are written.')
  parser.add_argument('-s', '--fluent-server', default="localhost", help='Address or hostname of the fluentd instance')
  parser.add_argument('-p', '--fluent-port', type=int, default=24224, help='Port of the fluentd instance')

  args = parser.parse_args()
  print(f'spawning log writers with args: {args}')
  run_test(
    args.num_writers,
    args.run_for_sec,
    args.events_per_sec,
    args.line_length,
    args.output_type,
    args.log_path,
    args.fluent_server,
    args.fluent_port
  )
