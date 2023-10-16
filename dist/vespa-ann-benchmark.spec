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

Name:           vespa-ann-benchmark
Version:        _VESPA_VERSION_
Release:        1%{?dist}
Summary:        Vespa - The open big data serving engine - ann-benchmark
Group:          Applications/Databases
License:        Commercial
URL:            http://vespa.ai
Source0:        vespa-ann-benchmark-%{version}.tar.gz

BuildRequires: vespa-build-dependencies = 1.0.1
BuildRequires: vespa-devel = %{version}-%{release}
%if 0%{?el8}
%global _centos_stream %(grep -qs '^NAME="CentOS Stream"' /etc/os-release && echo 1 || echo 0)
%define _devtoolset_enable /opt/rh/gcc-toolset-12/enable

%define _use_vespa_gtest 1
%define _use_vespa_openblas 1
%define _use_vespa_openssl 1
%define _use_vespa_protobuf 1

%if 0%{?centos} || 0%{?rocky} || 0%{?oraclelinux}
%define _command_cmake cmake
%endif

BuildRequires: vespa-pybind11-devel
BuildRequires: python39-devel
BuildRequires: python39-pip

Requires: python39

%endif

%if 0%{?el9}
%global _centos_stream %(grep -qs '^NAME="CentOS Stream"' /etc/os-release && echo 1 || echo 0)
%define _devtoolset_enable /opt/rh/gcc-toolset-12/enable
%define _use_vespa_protobuf 1

BuildRequires: pybind11-devel
BuildRequires: python3-pytest
BuildRequires: python3-devel
Requires: python3
%endif

%if 0%{?fedora}
BuildRequires: pybind11-devel
BuildRequires: python3-pytest
BuildRequires: python3-devel
Requires: python3
%endif

# For Amazon Linux 2023 fedora is also defined
%if 0%{?amzn2023}
%define _java_home /usr/lib/jvm/java-17-amazon-corretto
%define _use_vespa_re2 1
%define _use_vespa_xxhash 1
%endif

Requires: vespa-base-libs = %{version}-%{release}
Requires: vespa-libs = %{version}-%{release}

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
