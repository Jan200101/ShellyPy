# Created by pyp2rpm-3.3.2
%global pypi_name ShellyPy

Name:           python-%{pypi_name}
Version:        0.1.4
Release:        1%{?dist}
Summary:        Wrapper around the Shelly HTTP api

License:        MIT
URL:            https://github.com/Jan200101/ShellyPy
Source0:        https://files.pythonhosted.org/packages/source/S/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python2dist(setuptools)
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

%description
 ShellyPy not to be confused with [pyShelly]( Python 2 and 3 Wrapper around the
Shelly HTTP apiother packages like [pyShelly]( only support CoAP or MSQT,
neither I am comfortable with using in personal projects example here is a
simple working example for the Shelly 1 that turns a relay on python import
ShellyPydevice ShellyPy.Shelly("192.168.0.5")device.relay(0, turnTrue)this
example with...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python2dist(requests)
%description -n python2-%{pypi_name}
 ShellyPy not to be confused with [pyShelly]( Python 2 and 3 Wrapper around the
Shelly HTTP apiother packages like [pyShelly]( only support CoAP or MSQT,
neither I am comfortable with using in personal projects example here is a
simple working example for the Shelly 1 that turns a relay on python import
ShellyPydevice ShellyPy.Shelly("192.168.0.5")device.relay(0, turnTrue)this
example with...

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3dist(requests)
%description -n python3-%{pypi_name}
 ShellyPy not to be confused with [pyShelly]( Python 2 and 3 Wrapper around the
Shelly HTTP apiother packages like [pyShelly]( only support CoAP or MSQT,
neither I am comfortable with using in personal projects example here is a
simple working example for the Shelly 1 that turns a relay on python import
ShellyPydevice ShellyPy.Shelly("192.168.0.5")device.relay(0, turnTrue)this
example with...


%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%py2_install
%py3_install

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Mon Mar 09 2020 mockbuilder - 0.1.4-1
- Initial package.