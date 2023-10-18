# Copyright Vespa.ai. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.
TOP = $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

RPMTOPDIR=$(TOP)/rpmbuild
SOURCEDIR=$(RPMTOPDIR)/SOURCES
SPECDIR=$(RPMTOPDIR)/SPECS
SPECFILE=$(SPECDIR)/vespa-ann-benchmark-$(VESPA_VERSION).spec

deps:
	dnf install -y git rpmdevtools
	git config --global --add safe.directory $$(realpath $(TOP)/..)

srpm: VESPA_VERSION = $$(git tag --points-at HEAD | grep -oP "\d+\.\d+\.\d+" | sort -V | tail -1)
srpm: deps
	mkdir -p $(SPECDIR) $(SOURCEDIR)
	./dist.sh $(VESPA_VERSION)
	mv ~/rpmbuild/SOURCES/* $(SOURCEDIR)
	mv ~/rpmbuild/SPECS/* $(SPECDIR)
	spectool -g -C $(SOURCEDIR) $(SPECFILE)
	rpmbuild -bs --define "_topdir $(RPMTOPDIR)" $(SPECFILE)
	cp -a $(RPMTOPDIR)/SRPMS/* $(outdir)
clean:
	-rm -rf $(RPMTOPDIR)
rpm: srpm
	dnf builddep -y $(SPECFILE)
	rpmbuild --rebuild $(outdir)/vespa-ann-benchmark-$(VESPA_VERSION)-*src.rpm
	cp -a ~/rpmbuild/RPMS/*/*.rpm $(outdir)

.PHONY: srpm clean rpm
