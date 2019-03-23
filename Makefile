init:
	pip3 install --upgrade pipenv
	pipenv install --dev
install:
	pipenv install .
test:
	pipenv run sc -l fizzlebert
	pipenv run sc -t fizzlebert
	pipenv run sc -p coleur
	pipenv run sc -u https://soundcloud.com/fizzlebert/mad-world
