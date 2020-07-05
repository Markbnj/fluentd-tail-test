SHELL := /usr/bin/env bash -e

fluent_db_path := pos
num_writers ?= 1
run_for_sec ?= 10
events_per_sec ?= 50
line_length ?= 100
test_type ?= file
log_path ?= srclogs
fluent_host ?= localhost
fluent_port ?= 24224

.PHONY: help
help:
	@echo "Run 'make start' to launch services"
	@echo "Run 'make stop' to stop all services"
	@echo "Use 'make run-logs [var=value ...]' to run tests"
	@echo "Options:"
	@echo "    num_writers, number of processes to spawn (1)"
	@echo "    run_for_sec, number of seconds to generate logs (10)"
	@echo "    events_per_sec, number of log lines to emit per second (50)"
	@echo "    line_length, length in characters of the log lines (100)"
	@echo "    test_type, 'push' for network, or 'file' for tail"
	@echo "    log_path, output file path for tail tests (srclogs)"
	@echo "    fluent_host, address/hostname of fluentd for push tests (localhost)"
	@echo "    fluent_port, port of fluentd for push tests (24224)"

.venv:
	@python3 -m venv .venv &&\
	. .venv/bin/activate &&\
	pip install -r requirements.txt

.PHONY: .setup
.setup:
	@if [ ! -d $(output_path) ]; then\
		mkdir $(output_path);\
		chmod 777 $(output_path);\
	elif [ ! -z "$$(ls -A $(output_path))" ]; then\
		rm -f $(output_path)/*;\
	fi;\
	if [ ! -d $(fluent_db_path) ]; then\
		mkdir $(fluent_db_path);\
		chmod 777 $(fluent_db_path);\
	elif [ ! -z "$$(ls -A $(fluent_db_path))" ]; then\
		rm -f $(fluent_db_path)/*;\
	fi

.PHONY: .build-fluentd
.build-fluentd:
	@docker build -f Dockerfile.fluentd --rm --force-rm --tag fluentd:v1.10.4-debian-1.0-prom .

.PHONY: start
start: .build-fluentd .setup
	@docker-compose up -d
	@echo "Services running - access via the browser:"
	@echo "CAdvisor at http://localhost:8080"
	@echo "Prometheus at http://localhost:9090"
	@echo "Grafana at http://localhost:3000/login (user:fluent password:fluent)"

.PHONY: stop
stop:
	@docker-compose down

.PHONY: run-logs
run-logs: .venv
	@. .venv/bin/activate &&\
	export PYTHONPATH=$${PYTHONPATH}:./lib &&\
	python3 bin/test_runner.py\
	 --num-writers $(num_writers)\
	 --run-for $(run_for_sec)\
	 --events-per-sec $(events_per_sec)\
	 --line-length $(line_length)\
	 --output-type $(test_type)\
	 --log-path $(log_path)\
	 --fluent-server $(fluent_host)\
	 --fluent-port $(fluent_port)
