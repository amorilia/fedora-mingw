# NOTE: NOT a Fedora package.  This contains binaries which are needed
# just to bootstrap the whole system if you build everything from scratch.

%define runtime_version 3.14
%define w32api_version 3.11

Name:           mingw-bootstrap
Version:        1
Release:        1%{?dist}
Summary:        MinGW Windows bootstrap (binary package)

Group:          Development/Libraries
License:        Public Domain
URL:            http://www.mingw.org/

Source0:        http://dl.sourceforge.net/sourceforge/mingw/mingw-runtime-%{runtime_version}.tar.gz
Source1:        http://dl.sourceforge.net/sourceforge/mingw/w32api-%{w32api_version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       mingw-runtime = %{runtime_version}
Provides:       mingw-w32api = %{w32api_version}


%description
MinGW bootstrap (binary package).


%prep
%setup -q -c
%setup -q -D -T -a1


%build
rm -rf i686-pc-mingw32

# Setup sys-root.
mkdir -p i686-pc-mingw32/sys-root/mingw
cp -a include lib i686-pc-mingw32/sys-root/mingw


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}
cp -a i686-pc-mingw32 $RPM_BUILD_ROOT%{_prefix}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%dir %{_prefix}/i686-pc-mingw32
%{_prefix}/i686-pc-mingw32/sys-root


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1-1
- Initial RPM release.
