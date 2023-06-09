install:
	cp -r src ~/.local/share/nami2dpsg
	python -m venv ~/.local/share/nami2dpsg/.venv
	~/.local/share/nami2dpsg/.venv/bin/pip install -r requirements.txt
	cp -r nami2dpsg ~/.local/bin/

uninstall:
	rm -r ~/.local/share/nami2dpsg
	rm ~/.local/bin/nami2dpsg
