PY ?= .venv/bin/python

.PHONY: all build web serve venv clean

all: build web

venv:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

build:
	$(PY) scripts/build_dabfonts.py

web:
	$(PY) scripts/build_web_assets.py

serve:
	$(PY) scripts/serve.py 8099

clean:
	rm -rf build demo/fonts demo/dabfonts-demo.html
