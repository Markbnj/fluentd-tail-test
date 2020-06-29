SHELL := /usr/bin/env bash -e

output_path := srclogs
fluent_db_path := pos
num_writers ?= 1
run_for ?= 10
events_per_sec ?= 50


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

.PHONY: stop
stop:
	@docker-compose down

.PHONY: run-logs-tail
run-logs-tail:
	@python3 bin/test_runner.py\
	 --num-writers $(num_writers)\
	 --run-for $(run_for)\
	 --events-per-sec $(events_per_sec)\
	 --output-type file\
	 --path $(output_path)

.PHONY: run-logs-push
run-logs-push:
	@python3 bin/test_runner.py\
	 --num-writers $(num_writers)\
	 --run-for $(run_for)\
	 --events-per-sec $(events_per_sec)\
	 --output-type push
