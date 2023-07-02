.SECONDEXPANSION:


INSTALL_PATH := /usr/local
ifeq ($(origin XDG_CONFIG_HOME), undefined)
	CONFIG_HOME := ~/.config
else
	CONFIG_HOME := $(XDG_CONFIG_HOME)
endif


install: $(CONFIG_HOME)/nami2sepa/sepa_config.json $(INSTALL_PATH)/lib/nami2sepa $(INSTALL_PATH)/bin/nami2sepa

$(CONFIG_HOME)/nami2sepa/sepa_config.json: | $(CONFIG_HOME)/nami2sepa
	cp sepa_config.json $@

$(CONFIG_HOME)/nami2sepa:
	mkdir -p $@

$(INSTALL_PATH)/lib/nami2sepa: $$(subst src,$$@,$(wildcard src/*))
	mkdir -p $@
#	python -m venv $(INSTALL_PATH)/lib/nami2sepa/.venv
#	$(INSTALL_PATH)/lib/nami2sepa/.venv/bin/pip install -r requirements.txt

$(INSTALL_PATH)/lib/nami2sepa/%:
	cp src/$(@F) $@

$(INSTALL_PATH)/bin/nami2sepa:
	cp nami2sepa $@

uninstall:
	rm -r $(INSTALL_PATH)/lib/nami2sepa
	rm $(INSTALL_PATH)/bin/nami2sepa


.PHONY: install uninstall

