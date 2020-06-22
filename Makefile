SHELL := /usr/bin/env bash -e

output_path := srclogs
fluent_db_path := pos

.PHONY: .setup
.setup:
	@if [ ! -d $(output_path) ]; then\
		mkdir $(output_path);\
		chmod 777 $(output_path);\
	elif [ ! -z "$(ls -A $(output_path))" ]; then\
		rm -f $(output_path)/*;\
	fi;\
	if [ ! -d $(fluent_db_path) ]; then\
		mkdir $(fluent_db_path);\
		chmod 777 $(fluent_db_path);\
	elif [ ! -z "$(ls -A $(fluent_db_path))" ]; then\
		rm -f $fluent_db_path/*;\
	fi

.PHONY: start
start: .setup
	docker-compose up -d

.PHONY: stop
stop:
	docker-compose down

.PHONY: run-logs
run-logs:
	python3 bin/test_runner.py --num-writers 2 --run-for 60 --write-delay 50 --output-type file --path srclogs
