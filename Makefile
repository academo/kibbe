default:
	make clean
	make setup
	make build

setup:
	python3 -m venv env
	make activate
	make install

activate:
	. env/bin/activate

install:
	pip3 install -r requirements.txt

build:
	pyinstaller kibbe.py --onefile --exclude-module autopep8 --exclude-module flake8 

clean:
	rm -rf kibbe.spec
	rm -rf build
	rm -rf dist

minor-release: 
	./scripts/increment-version.sh -v minor
	
major-release: 
	./scripts/increment-version.sh -v major