.PHONY: build check previews lint install

build:      ## Regenerate every theme from src/palette.py
	python3 src/build.py

check:      ## Build + WCAG contrast report
	python3 src/build.py --check

previews:   ## Re-render README screenshots (needs pygments + playwright)
	python3 src/preview.py && node src/shoot.cjs

lint:       ## Shellcheck the scripts
	shellcheck -x -s bash install.sh update.sh uninstall.sh lib/dodo.sh

install:
	./install.sh
