.SECONDEXPANSION:


INSTALL_PATH := /usr/local
ifeq ($(origin XDG_CONFIG_HOME), undefined)
	CONFIG_HOME := ~/.config
else
	CONFIG_HOME := $(XDG_CONFIG_HOME)
endif


install: $(CONFIG_HOME)/nami2sepa/sepa_config.json $(INSTALL_PATH)/lib/nami2sepa/.venv $(INSTALL_PATH)/bin/nami2sepa 

$(CONFIG_HOME)/nami2sepa/sepa_config.json:
	install -d $(@D)
	install sepa_config.json $(@D)

$(INSTALL_PATH)/lib/nami2sepa/.venv: $$(@D)
	sudo python -m venv $@
	sudo $@/bin/pip install -r requirements.txt

$(INSTALL_PATH)/lib/nami2sepa:
	sudo install -m 755 -d $@
	sudo install -m 755 src/* $@

$(INSTALL_PATH)/bin/nami2sepa:
	sudo install nami2sepa /usr/local/bin

uninstall:
	sudo rm -r $(INSTALL_PATH)/lib/nami2sepa
	sudo rm $(INSTALL_PATH)/bin/nami2sepa


.PHONY: install uninstall

