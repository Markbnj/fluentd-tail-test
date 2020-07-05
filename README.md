# fluentd-tail-test

Provides a framework for profiling the cpu/memory utilization of [fluentd](https://www.fluentd.org/) in two common log source scenarios: 1) a setup in which containers log to stdout and fluentd tails the log files; and 2) a setup in which containers push logs in msgpack format directly to fluentd. In the code these are referred to as "file" and "push" output types respectively.

Fluentd is configured to accept logs from tail and forward (network) sources, and to discard all records so that we can focus on the resource costs of acquiring the log lines. CAdvisor is installed to monitor the fluentd container resource usage. Prometheus is installed and configured to scrape cadvisor. Finally grafana is installed and configured with a provisioned dashboard that shows the primary metrics of interest:

 - fluentd percent cpu usage
 - fluentd memory usage in bytes
 - fluentd total logs processed
 - fluentd logs handled per second

 Uses [fluent-logger-python](https://github.com/fluent/fluent-logger-python) to handle the push path.

## Notes on metrics resolution

CAadvisor and prometheus are not really profiling tools. In a production setup you'd be unlikely to be able to scrape often enough to capture data at a useful resolution for profiling. For the purpose of this test it works fine for a couple of reasons: 1) fluentd and the target are on the same network (i.e. connected to the same bridge), so the i/o portion of the scrape is about as fast as it gets, and overall it takes about .1s to scrape cadvisor; 2) I'm generating a constant load for a given period of time, and all I'm really interested in is the average cpu/memory use over that period; and lastly 3) it makes pretty nice graphs.

## Use

```
Run 'make start' to launch services
Run 'make stop' to stop all services
Use 'make run-logs [var=value ...]' to run tests
Options:
    num_writers, number of processes to spawn (1)
    run_for_sec, number of seconds to generate logs (10)
    events_per_sec, number of log lines to emit per second (50)
    line_length, length in characters of the log lines (100)
    test_type, 'push' for network, or 'file' for tail
    log_path, output file path for tail tests (srclogs)
    fluent_host, address/hostname of fluentd for push tests (localhost)
    fluent_port, port of fluentd for push tests (24224)
```

### Web stuff

After start the following things are available on localhost:

 - [CAdvisor](http://localhost:8080)
 - [Prometheus](http://localhost:9090)
 - [Grafana](http://localhost:3000/login) (user:fluent password:fluent)

