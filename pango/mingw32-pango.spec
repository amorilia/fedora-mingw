%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-pango
Version:        1.22.1
Release:        6%{?dist}
Summary:        MinGW Windows Pango library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.pango.org
Source0:        http://download.gnome.org/sources/pango/1.21/pango-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Native pango uses a %post script to generate this, but the
# pango-querymodules.exe binary is not something we can easily run on
# a Linux host. We could use wine but wine isn't happy in a mock
# environment. So we just include a pre-generated copy on basis that
# it won't ever change much.
#
# If you want to rebuild this, do:
# wine %{_mingw32_bindir}/pango-querymodules.exe > pango.modules
Source1:        pango.modules

Patch1000:      pango_enable_static_build.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-cairo >= 1.8.0
BuildRequires:  mingw32-expat
BuildRequires:  mingw32-fontconfig
BuildRequires:  mingw32-freetype
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-glib2
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-pixman
BuildRequires:  pkgconfig

# Required in order to rebuild the configure script.
BuildRequires:  gtk-doc

# These are required for the patch
BuildRequires:  autoconf, automake, libtool

Requires:       pkgconfig


%description
MinGW Windows Pango library.


%package static
Summary:        Static version of the MinGW Windows Pango library
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description static
Static version of the MinGW Windows Pango library.


%prep
%setup -q -n pango-%{version}
%patch1000

# Regenerate the configure script
aclocal
autoreconf
libtoolize


%build
# Need to run the correct version of glib-mkenums.
PATH=%{_mingw32_bindir}:$PATH \
%{_mingw32_configure} --enable-static --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pango/
cp %{SOURCE1} $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/pango/

rm -f $RPM_BUILD_ROOT/%{_mingw32_libdir}/charset.alias


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{_mingw32_bindir}/libpango-1.0-0.dll
%{_mingw32_bindir}/libpangocairo-1.0-0.dll
%{_mingw32_bindir}/libpangoft2-1.0-0.dll
%{_mingw32_bindir}/libpangowin32-1.0-0.dll
%{_mingw32_bindir}/pango-querymodules.exe
%{_mingw32_includedir}/pango-1.0/
%{_mingw32_libdir}/libpango-1.0.dll.a
%{_mingw32_libdir}/libpango-1.0.la
%{_mingw32_libdir}/libpangocairo-1.0.dll.a
%{_mingw32_libdir}/libpangocairo-1.0.la
%{_mingw32_libdir}/libpangoft2-1.0.dll.a
%{_mingw32_libdir}/libpangoft2-1.0.la
%{_mingw32_libdir}/libpangowin32-1.0.dll.a
%{_mingw32_libdir}/libpangowin32-1.0.la
%{_mingw32_libdir}/pango-1.0.def
%{_mingw32_libdir}/pangocairo-1.0.def
%{_mingw32_libdir}/pangoft2-1.0.def
%{_mingw32_libdir}/pangowin32-1.0.def
%dir %{_mingw32_libdir}/pango
%dir %{_mingw32_libdir}/pango/1.6.0
%dir %{_mingw32_libdir}/pango/1.6.0/modules
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-win32.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-win32.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-win32.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-lang.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-lang.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-lang.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-lang.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-lang.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-lang.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hangul-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hangul-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hangul-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hebrew-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hebrew-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hebrew-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-khmer-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-khmer-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-khmer-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-syriac-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-syriac-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-syriac-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-thai-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-thai-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-thai-fc.la
%{_mingw32_libdir}/pango/1.6.0/modules/pango-tibetan-fc.dll
%{_mingw32_libdir}/pango/1.6.0/modules/pango-tibetan-fc.dll.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-tibetan-fc.la
%{_mingw32_libdir}/pkgconfig/pango.pc
%{_mingw32_libdir}/pkgconfig/pangocairo.pc
%{_mingw32_libdir}/pkgconfig/pangoft2.pc
%{_mingw32_libdir}/pkgconfig/pangowin32.pc
%{_mingw32_datadir}/gtk-doc/html/pango/
%{_mingw32_mandir}/man1/pango-querymodules.1*
%{_mingw32_sysconfdir}/pango/


%files static
%defattr(-,root,root,-)
%{_mingw32_libdir}/libpango-1.0.a
%{_mingw32_libdir}/libpangocairo-1.0.a
%{_mingw32_libdir}/libpangoft2-1.0.a
%{_mingw32_libdir}/libpangowin32-1.0.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-win32.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-lang.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-lang.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-arabic-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-basic-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hangul-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-hebrew-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-indic-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-khmer-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-syriac-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-thai-fc.a
%{_mingw32_libdir}/pango/1.6.0/modules/pango-tibetan-fc.a
  

%changelog
* Fri Feb 20 2009 Erik van Pienbroek <info@nntpgrab.nl> - 1.22.1-6
- Added -static subpackage

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.22.1-5
- Rebuild for mingw32-gcc 4.4

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.22.1-4
- Requires pkgconfig.

* Tue Jan 27 2009 Levente Farkas <lfarkas@lfarkas.org> - 1.22.1-3
- Include license file in documentation section.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.22.1-2
- Disable static libraries.
- Use _smp_mflags.

* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.22.1-1
- New upstream version 1.22.1.
- BR cairo >= 1.8.0 because of important fixes.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.21.6-6
- Rename mingw -> mingw32.

* Tue Sep 23 2008 Daniel P. Berrange <berrange@redhat.com> - 1.21.6-5
- Remove use of wine in %-post.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.21.6-4
- Add dep on pkgconfig

* Thu Sep 11 2008 Richard W.M. Jones <rjones@redhat.com> - 1.21.6-3
- post/preun scripts to update the pango.modules list.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.21.6-2
- Run the correct glib-mkenums.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.21.6-1
- Initial RPM release
