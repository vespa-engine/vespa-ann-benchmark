FROM quay.io/centos/centos:stream8

RUN dnf -y install epel-release && \
    dnf -y install dnf-plugins-core && \
    dnf -y copr enable @vespa/vespa centos-stream-8 

RUN --mount=type=bind,target=/include,source=.,ro \
    dnf -y module enable maven:3.8 && \
    dnf -y localinstall --enablerepo=powertools /include/vespa-ann-benchmark-[0-9].*.$(arch).rpm
