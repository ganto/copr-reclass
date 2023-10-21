%global srcname reclass

Name:           python-%{srcname}
Version:        1.7.0
Release:        0.1%{?dist}
Summary:        A recursive external node classifier for configuration management systems
License:        Artistic-1.0-Perl
URL:            https://github.com/salt-formulas/reclass
Source0:        https://github.com/salt-formulas/reclass/archive/refs/tags/v%{version}.tar.gz#/reclass-v%{version}.tar.gz
Patch0:         v1.7.0-Add-support-for-collections.abc-in-Python-gt-3.8.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-pyparsing
BuildRequires:  python3-pyyaml
BuildRequires:  python3-six
BuildRequires:  make
BuildRequires:  python3-sphinx
BuildRequires:  python3dist(pytest)
BuildRequires:  python3-ddt
BuildRequires:  python3-mock

%global _description %{expand:
reclass is an "external node classifier" (ENC) as can be used with automation
tools, such as Puppet, Salt, and Ansible. It is also a stand-alone tool for
merging data sources recursively.}

%description %_description

%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}

# disable unneeded runtime dependencies
sed -i -e '/enum34/d' -e '/ddt/d' Pipfile requirements.txt
sed -i -e "s/, 'enum34'//" -e "s/, 'ddt'//" setup.py

%build
%pyproject_wheel
pushd doc
make man
popd

%install
%pyproject_install
%pyproject_save_files %{srcname}
install -d %{buildroot}%{_mandir}/man1
cp -p doc/build/man/%{srcname}.1 %{buildroot}%{_mandir}/man1/

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst README-extensions.rst
%{_bindir}/*
%{_mandir}/man1/%{srcname}.1.*

%changelog
