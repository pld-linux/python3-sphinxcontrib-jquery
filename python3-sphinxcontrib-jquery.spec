# Conditional build:
%bcond_with	tests	# unit tests

%define		module	sphinxcontrib-jquery
Summary:	Extension to include jQuery on newer Sphinx releases
Name:		python3-%{module}
Version:	4.1
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.debian.net/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	46ea52845b17343ed6c61e6963fb265d
URL:		https://pypi.org/project/sphinxcontrib-jquery/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
# replace with other requires if defined in setup.py
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ensures that jQuery is always installed for use in Sphinx themes or
extensions.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENCE README.rst
%{py3_sitescriptdir}/sphinxcontrib/jquery
%{py3_sitescriptdir}/sphinxcontrib_jquery-%{version}.dist-info
