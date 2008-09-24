%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-atk
Version:        1.24.0
Release:        2%{?dist}
Summary:        MinGW Windows Atk library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://developer.gnome.org/projects/gap/
Source:         http://download.gnome.org/sources/atk/1.24/atk-%{version}.tar.bz2 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-glib2
BuildRequires:  pkgconfig
# Need native one too for msgfmt
BuildRequires:  gettext
# Need native one too for  glib-genmarshal
BuildRequires:  glib2-devel


%description
MinGW Windows Atk library.


%prep
%setup -q -n atk-%{version}


%build
%{_mingw32_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw32_libdir}/charset.alias


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libatk-1.0-0.dll
%{_mingw32_includedir}/atk-1.0
%{_mingw32_libdir}/atk-1.0.def
%{_mingw32_libdir}/libatk-1.0.dll.a
%{_mingw32_libdir}/libatk-1.0.la
%{_mingw32_libdir}/pkgconfig/atk.pc
%{_mingw32_datadir}/gtk-doc/html/atk/
%{_mingw32_datadir}/locale/*/LC_MESSAGES/atk10.mo


%changelog
* Wed Sep 24 2008 Daniel P. Berrange <berrange@redhat.com> - 1.24.0-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.24.0-1
- Update to 1.24.0 release

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.23.5-2
- Added dep on pkgconfig and glib2-devel (native)

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.23.5-1
- Initial RPM release
