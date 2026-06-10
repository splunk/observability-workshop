PYTHON ?= python3

.PHONY: test test-python splunk-render splunk-apply

test: test-python

test-python:
	$(PYTHON) -m unittest tests/test_sync_splunk_objects.py

splunk-render:
	$(PYTHON) infra/splunk/sync_splunk_objects.py

splunk-apply:
	$(PYTHON) infra/splunk/sync_splunk_objects.py --apply
