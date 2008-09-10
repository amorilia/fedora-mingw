%include /usr/lib/rpm/mingw-defs

Name:           mingw-atk
Version:        1.23.5
Release:        1%{?dist}
Summary:        MinGW Windows Atk library

License: LGPLv2+
Group:          Development/Libraries
URL: http://developer.gnome.org/projects/gap/
Source: http://download.gnome.org/sources/atk/1.23/atk-%{version}.tar.bz2 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch1: atk-%{version}-mingw.patch

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-iconv
BuildRequires:  mingw-gettext
BuildRequires:  mingw-glib2

%description
MinGW Windows Atk library.


%prep
%setup -q -n atk-%{version}
%patch1 -p1

%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw_libdir}/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/libatk-1.0-0.dll
%{_mingw_includedir}/atk-1.0
%{_mingw_libdir}/atk-1.0.def
%{_mingw_libdir}/libatk-1.0.dll.a
%{_mingw_libdir}/libatk-1.0.la
%{_mingw_libdir}/pkgconfig/atk.pc
%{_mingw_datadir}/gtk-doc/html/atk/
%{_mingw_datadir}/locale/*/LC_MESSAGES/atk10.mo

%changelog
* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.23.5-1
- Initial RPM release
