%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-atk
Version:        1.25.2
Release:        1%{?dist}
Summary:        MinGW Windows Atk library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://projects.gnome.org/accessibility/
Source:         http://ftp.gnome.org/pub/GNOME/sources/atk/1.25/atk-%{version}.tar.bz2
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
%{_mingw32_configure} --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT/%{_mingw32_libdir}/charset.alias

%find_lang atk10

%clean
rm -rf $RPM_BUILD_ROOT


%files -f atk10.lang
%defattr(-,root,root)
%{_mingw32_bindir}/libatk-1.0-0.dll
%{_mingw32_includedir}/atk-1.0
%{_mingw32_libdir}/atk-1.0.def
%{_mingw32_libdir}/libatk-1.0.dll.a
%{_mingw32_libdir}/libatk-1.0.la
%{_mingw32_libdir}/pkgconfig/atk.pc
%{_mingw32_datadir}/gtk-doc/html/atk/


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.25.2-1
- Rebase to latest Fedora native version 1.25.2.
- Use find_lang macro.
- Use smp_mflags.
- Fix URL.
- Fix Source URL.

* Wed Sep 24 2008 Daniel P. Berrange <berrange@redhat.com> - 1.24.0-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.24.0-1
- Update to 1.24.0 release

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.23.5-2
- Added dep on pkgconfig and glib2-devel (native)

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.23.5-1
- Initial RPM release
