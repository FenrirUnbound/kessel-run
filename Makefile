test: venv lib
	. venv/bin/activate; nosetests -v ./tests

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
