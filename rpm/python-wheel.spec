# TODO package pytest
%bcond_with run_tests

# suffix of python executable (not defined at OBS)
%global python3_pkgversion 3

%global DISTNAME wheel
# OBS doesn't allow macro in Name
Name:           python-wheel
Version:        0.37.1
Release:        1%{?dist}
Summary:        Built-package format for Python
License:        MIT
URL:            https://github.com/pypa/wheel
Source:         %{name}-%{version}.tar.bz2
BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
# not present while bootstrapping python3: 
BuildRequires:  python%{python3_pkgversion}-rpm-generators
%if %{with run_tests}
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  gcc
%endif
# fix wrong dep:
%global __requires_exclude ^python3dist\\(pygobject\\)$

%global _description %{expand:
The reference implementation of the Python wheel packaging standard, as defined
in PEP 427.

It has two different roles:

 1. A setuptools extension for building wheels that provides the bdist_wheel
    setuptools command.
 2. A command line tool for working with wheel files.}

%description %{_description}

%prep
%autosetup -n %{name}-%{version}/wheel

%build
%py3_build

%if %{with run_tests}
%check
%pytest
%endif

%install
%py3_install
mv %{buildroot}%{_bindir}/%{DISTNAME}{,-%{python3_version}}
ln -s %{DISTNAME}-%{python3_version} %{buildroot}%{_bindir}/%{DISTNAME}-3
ln -s %{DISTNAME}-%{python3_version} %{buildroot}%{_bindir}/%{DISTNAME}


%package -n     python%{python3_pkgversion}-%{DISTNAME}
Summary:        %{summary}
%description -n python%{python3_pkgversion}-%{DISTNAME} %{_description}

This is the setuptools extension.
%if "%{?vendor}" == "chum"
Type: addon
PackagerName: takimata
Categories:
 - Development
%endif

%files -n       python%{python3_pkgversion}-%{DISTNAME}
%license LICENSE.txt
%{python3_sitelib}/%{DISTNAME}*/


%package -n     python%{python3_pkgversion}-%{DISTNAME}-tools
Summary:        %{summary} (tools)
%description -n python%{python3_pkgversion}-%{DISTNAME}-tools %{_description}

This is the command line tool and documentation.
%if "%{?vendor}" == "chum"
Type: console-application
PackagerName: takimata
Categories:
 - Development
 - Utility
%endif

%files -n       python%{python3_pkgversion}-%{DISTNAME}-tools
%doc manpages/*.rst
%{_bindir}/%{DISTNAME}-%{python3_version}
%{_bindir}/%{DISTNAME}-3
%{_bindir}/%{DISTNAME}


%changelog
* Mon May 09 2022 takimata <takimata@gmx.de> - 0.37.1-1
- Initial packaging for Chum
