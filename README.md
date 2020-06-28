# fluentd-tail-test

Provides a framework for testing the cpu/memory utilization of [fluentd](https://www.fluentd.org/) in a typical kubernetes cluster logging scenario where some number of containers are logging to stdout, which containerd is redirecting to a file that is symlinked in /var/log/containers. Fluentd is configured to tail log files and discard all records so we can focus on the costs of acquiring the lines. CAdvisor is installed to monitor the fluentd container resource usage. Prometheus is installed to scrape usage metrics from cadvisor. Grafana is installed to visualize the data in prometheus.

## Use

`make start` - builds a fluentd image with the prometheus plugin, then launches cadvisor, fluentd, prometheus and grafana.
`make run-logs` - spawns log writers
`make stop` - shuts down all containers

### Web stuff

After start the following things are available on localhost:

 - [CAdvisor](http://localhost:8080)
 - [Prometheus](http://localhost:9090)
 - [Grafana](http://localhost:3000/login) (user:fluent password:fluent)

For the purposes of these tests only grafana is of immediate use. It includes a provisioned dashboard that tracks fluentd container cpu use, memory and total records processed.
