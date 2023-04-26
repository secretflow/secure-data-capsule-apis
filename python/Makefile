init:
	pip install -r requirements.txt

build:
	python ../protoc.py
	find ./secretflowapis -maxdepth 10 -type d -exec cp __init__.py {} \;
	python setup.py clean
	python setup.py sdist bdist_wheel
	twine check dist/*

upload:
	twine upload -r pypiantfin dist/*

rebuild:
	make clean
	make build

clean:
	rm -rf build
	rm -rf secretflowapis*
	rm -rf dist
