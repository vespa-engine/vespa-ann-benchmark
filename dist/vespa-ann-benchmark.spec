# Copyright Yahoo. Licensed under the terms of the Apache 2.0 license. See LICENSE in the project root.

# Only strip debug info
%global _find_debuginfo_opts -g

# Don't enable LTO
%global _lto_cflags %{nil}

# Disable hardened package build.
%global _preprocessor_defines %{nil}
%undefine _hardened_build

# Libraries and binaries use shared libraries in /opt/vespa/lib64 and
# /opt/vespa-deps/lib64
%global __brp_check_rpaths %{nil}

# Force special prefix for Vespa
%define _prefix /opt/vespa
%define _command_cmake cmake3

Name:           vespa-ann-benchmark-testing
Version:        _VESPA_VERSION_
Release:        1%{?dist}
Summary:        Vespa - The open big data serving engine - ann-benchmark
Group:          Applications/Databases
License:        Commercial
URL:            http://vespa.ai
Source0:        vespa-ann-benchmark-%{version}.tar.gz

%if 0%{?centos} || 0%{?rocky} || 0%{?oraclelinux}
BuildRequires: epel-release
%endif
%if 0%{?el8}
%global _centos_stream %(grep -qs '^NAME="CentOS Stream"' /etc/os-release && echo 1 || echo 0)
BuildRequires: gcc-toolset-12-gcc-c++
BuildRequires: gcc-toolset-12-binutils
BuildRequires: gcc-toolset-12-libatomic-devel
%define _devtoolset_enable /opt/rh/gcc-toolset-12/enable
BuildRequires: maven
BuildRequires: maven-openjdk17
BuildRequires: vespa-pybind11-devel
BuildRequires: python39-devel
BuildRequires: python39-pip
BuildRequires: glibc-langpack-en
%endif
%if 0%{?el9}
%global _centos_stream %(grep -qs '^NAME="CentOS Stream"' /etc/os-release && echo 1 || echo 0)
BuildRequires: gcc-toolset-12-gcc-c++
BuildRequires: gcc-toolset-12-binutils
BuildRequires: gcc-toolset-12-libatomic-devel
%define _devtoolset_enable /opt/rh/gcc-toolset-12/enable
BuildRequires: pybind11-devel
BuildRequires: python3-pytest
BuildRequires: python3-devel
BuildRequires: glibc-langpack-en
%endif
%if 0%{?fedora}
BuildRequires: gcc-c++
BuildRequires: libatomic
BuildRequires: pybind11-devel
BuildRequires: python3-pytest
BuildRequires: python3-devel
BuildRequires: glibc-langpack-en
%endif
%if 0%{?el8}
BuildRequires: cmake >= 3.11.4-3
%if 0%{?centos} || 0%{?rocky} || 0%{?oraclelinux}
%if 0%{?centos}
# Current cmake on CentOS 8 is broken and manually requires libarchive install
BuildRequires: libarchive
%endif
%define _command_cmake cmake
%endif
BuildRequires: llvm-devel
BuildRequires: vespa-boost-devel >= 1.76.0-1
BuildRequires: vespa-openssl-devel >= 1.1.1o-1
%define _use_vespa_openssl 1
BuildRequires: vespa-gtest = 1.13.0
%define _use_vespa_gtest 1
BuildRequires: vespa-lz4-devel >= 1.9.4-1
BuildRequires: vespa-onnxruntime-devel = 1.15.1
BuildRequires: vespa-protobuf-devel = 3.21.12
%define _use_vespa_protobuf 1
BuildRequires: vespa-libzstd-devel >= 1.5.4-1
%endif
%if 0%{?el9}
BuildRequires: cmake >= 3.20.2
BuildRequires: maven
BuildRequires: maven-openjdk17
BuildRequires: openssl-devel
BuildRequires: vespa-lz4-devel >= 1.9.4-1
BuildRequires: vespa-onnxruntime-devel = 1.15.1
BuildRequires: vespa-libzstd-devel >= 1.5.4-1
BuildRequires: vespa-protobuf-devel = 3.21.12
%define _use_vespa_protobuf 1
BuildRequires: llvm-devel
BuildRequires: boost-devel >= 1.75
BuildRequires: gtest-devel
BuildRequires: gmock-devel
%endif
%if 0%{?fedora}
BuildRequires: cmake >= 3.9.1
BuildRequires: maven
%if 0%{?amzn2023}
BuildRequires: maven-amazon-corretto17
%define _java_home /usr/lib/jvm/java-17-amazon-corretto
%else
%if %{?fedora} >= 35
BuildRequires: maven-openjdk17
%endif
%endif
BuildRequires: openssl-devel
BuildRequires: vespa-lz4-devel >= 1.9.4-1
BuildRequires: vespa-onnxruntime-devel = 1.15.1
BuildRequires: vespa-libzstd-devel >= 1.5.4-1
BuildRequires: protobuf-devel
BuildRequires: llvm-devel
BuildRequires: boost-devel
BuildRequires: gtest-devel
BuildRequires: gmock-devel
%endif
%if 0%{?amzn2023}
BuildRequires: vespa-xxhash-devel >= 0.8.1
%define _use_vespa_xxhash 1
%else
BuildRequires: xxhash-devel >= 0.8.1
%endif
%if 0%{?el8}
BuildRequires: vespa-openblas-devel >= 0.3.21
%define _use_vespa_openblas 1
%else
BuildRequires: openblas-devel
%endif
%if 0%{?amzn2023}
BuildRequires: vespa-re2-devel = 20210801
%define _use_vespa_re2 1
%else
BuildRequires: re2-devel
%endif
BuildRequires: zlib-devel
BuildRequires: libicu-devel
%if 0%{?amzn2023}
BuildRequires: java-17-amazon-corretto-devel
BuildRequires: java-17-amazon-corretto
%else
BuildRequires: java-17-openjdk-devel
%endif
BuildRequires: rpm-build
BuildRequires: make
BuildRequires: git
BuildRequires: golang
BuildRequires: systemd
BuildRequires: flex >= 2.5.0
BuildRequires: bison >= 3.0.0
BuildRequires: libedit-devel

BuildRequires: vespa = %{version}-%{release}

Requires: vespa-base-libs = %{version}-%{release}
Requires: vespa-libs = %{version}-%{release}
%if 0%{?el8}
Requires: python39
%endif
%if 0%{?el9}
Requires: python3
%endif
%if 0%{?fedora}
Requires: python3
%endif

# Ugly workaround because vespamalloc/src/vespamalloc/malloc/mmap.cpp uses the private
# _dl_sym function.
# Exclude automated requires for libraries in /opt/vespa-deps/lib64.
%global __requires_exclude ^lib(c\\.so\\.6\\(GLIBC_PRIVATE\\)|pthread\\.so\\.0\\(GLIBC_PRIVATE\\)|(lz4%{?_use_vespa_protobuf:|protobuf}|zstd|onnxruntime%{?_use_vespa_openssl:|crypto|ssl}%{?_use_vespa_openblas:|openblas}%{?_use_vespa_re2:|re2}%{?_use_vespa_xxhash:|xxhash}%{?_use_vespa_gtest:|(gtest|gmock)(_main)?})\\.so\\.[0-9.]*\\([A-Za-z._0-9]*\\))\\(64bit\\)$

%description

Vespa - The open big data serving engine - ann-benchmark

Python binding for the Vespa implementation of an HNSW index for
nearest neighbor search used for low-level benchmarking.

%prep
%setup -q -n vespa-ann-benchmark-%{version}

%build
%if 0%{?_devtoolset_enable:1}
source %{_devtoolset_enable} || true
%endif

%{_command_cmake} -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DVESPA_UNPRIVILEGED=no \
       .

%check
%if 0%{?el8}
python3.9 -m pip install --user pytest
%endif
export PYTHONPATH="$PYTHONPATH:/usr/local/lib/$(basename $(readlink -f $(which python3)))/site-packages"
make test ARGS="--output-on-failure %{_smp_mflags}"

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %{_prefix}
%dir %{_prefix}/libexec
%{_prefix}/libexec/vespa_ann_benchmark

%changelog
