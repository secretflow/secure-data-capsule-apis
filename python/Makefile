init:
	uv sync --group dev

build:
	uv run python ../protoc.py
	touch ./secretflowapis/__init__.py
	python -c "from datetime import date; v='0.4.0.dev'+date.today().strftime('%Y%m%d'); open('_version.py','w').write(f'__version__ = \"{v}\"\n')"
	uv build
	uv run twine check dist/*

rebuild:
	make clean
	make build

clean:
	rm -rf build
	rm -rf secretflowapis*
	rm -rf dist