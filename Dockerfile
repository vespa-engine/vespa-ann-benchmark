FROM almalinux:10

RUN dnf -y install epel-release && \
    dnf -y install dnf-plugins-core && \
    dnf config-manager --add-repo https://raw.githubusercontent.com/vespa-engine/vespa/master/dist/vespa-engine.repo

RUN --mount=type=bind,target=/include,source=.,ro \
    dnf -y module enable maven:3.8 && \
    echo "================================================" && \
    ls -lA /include/ && \
    echo "================================================" && \
    echo "$(arch)" && \
    echo "================================================" && \
    dnf -y localinstall --enablerepo=powertools /include/vespa-ann-benchmark-[0-9].*.$(arch).rpm
