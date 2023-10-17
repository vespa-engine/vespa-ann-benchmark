# Copyright Vespa.ai. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.
TOP = $(realpath $(dir $(lastword $(MAKEFILE_LIST))))

# Version
VESPA_VERSION ?= 8.241.13

RPMTOPDIR=$(TOP)/rpmbuild
SOURCEDIR=$(RPMTOPDIR)/SOURCES
SPECDIR=$(RPMTOPDIR)/SPECS
SPECFILE=$(SPECDIR)/vespa-ann-benchmark-$(VESPA_VERSION).spec

srpm:
	rpm -q rpmdevtools || dnf install -y rpmdevtools
	mkdir -p $(SPECDIR) $(SOURCEDIR)
	#sed -e "s,_VESPA_VERSION_,$(VESPA_VERSION),g" dist/vespa-ann-benchmark.spec > $(SPECFILE)
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
