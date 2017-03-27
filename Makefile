
ENV=env/bin

all: env
	mypy bevos --strict-optional
	nose2 tests

env:
	python3 -m venv env; \
	source env/bin/activate; \

install: requirements.txt env
	$(ENV)/pip install -r requirements.txt
	$(ENV)/pip install --editable .

activate:
	source "source env/bin/activate"; \

clean:
	deactivate
	rm -rf env
	rm -rf bevos.egg-info

# check:
# 	python3 -m venv env
# 	. env/bin/activate
