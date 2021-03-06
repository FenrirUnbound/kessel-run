ifeq ("${CI}","true")
  SDK_PATH=./google_appengine
else
  SDK_PATH="$(HOME)/Git/google-cloud-sdk/platform/google_appengine"
endif

test: venv lib
	. venv/bin/activate; nosetests --with-gae --gae-lib-root=${SDK_PATH} -v ./tests

clean:
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf venv || echo "";
	rm -rf lib || echo "";

venv/bin/activate: dev_requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur dev_requirements.txt
	touch venv/bin/activate
venv: venv/bin/activate

lib: venv requirements.txt
	. venv/bin/activate; pip install -t lib -Ur requirements.txt

local: lib
	dev_appserver.py app.yaml

deploy: clean
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -t lib -Ur requirements.txt
	touch venv/bin/activate
	. venv/bin/activate; gcloud app deploy app.yaml index.yaml cron.yaml --project kesselrun-iv
