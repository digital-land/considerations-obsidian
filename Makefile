.PHONY: wiki all init clean clobber
.SECONDARY:

CACHE_DIR=var/cache/

all: wiki

wiki:	$(CACHE_DIR)planning-considerations.csv
	python3 bin/wiki.py

# download a dataset
$(CACHE_DIR)dataset/%.csv: 
	@mkdir -p $(dir $@)
	curl -qLfs 'https://files.planning.data.gov.uk/dataset/$(@F)' > $@

# download organisations
$(CACHE_DIR)organisation.csv: 
	@mkdir -p $(dir $@)
	curl -qLfs 'https://files.planning.data.gov.uk/organisation-collection/dataset/organisation.csv' > $@

# download considerations
$(CACHE_DIR)planning-considerations.csv: 
	@mkdir -p $(dir $@)
	curl -qLfs 'https://design.planning.data.gov.uk/planning-consideration/planning-considerations.csv' > $@

init::
	pip install -r requirements.txt

clean::
	rm -rf var/ wiki/Consideration/
