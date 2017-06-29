ifeq ("${CI}","true")
  SDK_PATH=./google_appengine
else
  SDK_PATH="$(HOME)/google-cloud-sdk"
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

deploy: clean
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -t lib -Ur requirements.txt
	touch venv/bin/activate
	. venv/bin/activate; gcloud app deploy app.yaml --project kesselrun-iv
