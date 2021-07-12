default:
	make clean
	make setup
	make build

setup:
	make activate
	make install

activate:
	. env/bin/activate

install:
	pip3 install -r requirements.txt

build:
	./env/bin/pyinstaller kibbe.py --onefile

clean:
	rm -rf kibbe.spec
	rm -rf build
	rm -rf dist
