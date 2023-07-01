install:
	mkdir .config/nami2sepa
	cp -r src ~/.local/share/nami2sepa
	python -m venv ~/.local/share/nami2sepa/.venv
	~/.local/share/nami2sepa/.venv/bin/pip install -r requirements.txt
	cp nami2sepa ~/.local/bin/

uninstall:
	rm -r ~/.local/share/nami2sepa
	rm ~/.local/bin/nami2sepa

install_dev:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt
