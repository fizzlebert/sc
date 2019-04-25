init:
	pip3 install --upgrade pipenv
	pipenv install --dev
install:
	pipenv install .
test:
	sc -l fizzlebert
	sc -t fizzlebert
	sc -p coleur
	sc -u https://soundcloud.com/fizzlebert/mad-world
