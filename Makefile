setup:
	python3 -m venv env
	make activate
	make install

activate:
	. env/bin/activate

install:
	pip3 install -r requirements.txt

build:
	make setup
	pip3 install pyinstaller
	pyinstaller kibbe.py -n $(name) --onefile --exclude-module autopep8 --exclude-module flake8 

clean:
	rm -rf kibbe.spec
	rm -rf build
	rm -rf dist

minor-release: 
	./scripts/increment-version.sh -v minor
	
major-release: 
	./scripts/increment-version.sh -v major
	
publish-pip:
	make clean
	make setup
	pip3 install twine
	python3 setup.py sdist
	twine upload -u __token__ -p $(token) --disable-progress-bar --skip-existing  --non-interactive dist/*