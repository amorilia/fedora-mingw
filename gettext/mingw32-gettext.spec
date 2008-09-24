%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:      mingw32-gettext
Version:   0.17
Release:   5%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/gettext/
Source0:   http://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: mingw32-filesystem >= 23
BuildRequires: mingw32-gcc
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-binutils
BuildRequires: mingw32-iconv


%description
MinGW Windows Gettext library

%prep
%setup -q -n gettext-%{version}

%build
%{_mingw32_configure} \
  --disable-java \
  --disable-native-java \
  --disable-csharp \
  --enable-threads=win32 \
  --without-emacs

make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_mingw32_datadir}/locale/locale.alias
rm -f $RPM_BUILD_ROOT%{_mingw32_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{_mingw32_datadir}/info/dir

# Remove static libraries.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libasprintf.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgettextpo.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libintl.a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_mingw32_bindir}/autopoint
%{_mingw32_bindir}/envsubst.exe
%{_mingw32_bindir}/gettext.exe
%{_mingw32_bindir}/gettext.sh
%{_mingw32_bindir}/gettextize
%{_mingw32_bindir}/libasprintf-0.dll
%{_mingw32_bindir}/libgettextlib-0-17.dll
%{_mingw32_bindir}/libgettextpo-0.dll
%{_mingw32_bindir}/libgettextsrc-0-17.dll
%{_mingw32_bindir}/libintl-8.dll
%{_mingw32_bindir}/msg*.exe
%{_mingw32_bindir}/ngettext.exe
%{_mingw32_bindir}/recode-sr-latin.exe
%{_mingw32_bindir}/xgettext.exe

%{_mingw32_includedir}/autosprintf.h
%{_mingw32_includedir}/gettext-po.h
%{_mingw32_includedir}/libintl.h

%{_mingw32_libdir}/gettext

%{_mingw32_libdir}/libasprintf.dll.a
%{_mingw32_libdir}/libasprintf.la

%{_mingw32_libdir}/libgettextlib.dll.a
%{_mingw32_libdir}/libgettextlib.la

%{_mingw32_libdir}/libgettextpo.dll.a
%{_mingw32_libdir}/libgettextpo.la

%{_mingw32_libdir}/libgettextsrc.dll.a
%{_mingw32_libdir}/libgettextsrc.la

%{_mingw32_libdir}/libintl.dll.a
%{_mingw32_libdir}/libintl.la

%{_mingw32_docdir}/gettext
%{_mingw32_docdir}/libasprintf/autosprintf_all.html

%{_mingw32_datadir}/gettext/

%{_mingw32_datadir}/aclocal/*m4
%{_mingw32_datadir}/info/autosprintf.info
%{_mingw32_datadir}/info/gettext.info

%{_mingw32_datadir}/locale/*/LC_MESSAGES/gettext-tools.mo
%{_mingw32_datadir}/locale/*/LC_MESSAGES/gettext-runtime.mo

%{_mingw32_mandir}/man1/autopoint.1*
%{_mingw32_mandir}/man1/envsubst.1*
%{_mingw32_mandir}/man1/gettext.1*
%{_mingw32_mandir}/man1/gettextize.1*
%{_mingw32_mandir}/man1/msg*1*
%{_mingw32_mandir}/man1/ngettext.1*
%{_mingw32_mandir}/man1/recode-sr-latin.1*
%{_mingw32_mandir}/man1/xgettext.1*

%{_mingw32_mandir}/man3/bind_textdomain_codeset.3*
%{_mingw32_mandir}/man3/bindtextdomain.3*
%{_mingw32_mandir}/man3/dcgettext.3*
%{_mingw32_mandir}/man3/dcngettext.3*
%{_mingw32_mandir}/man3/dgettext.3*
%{_mingw32_mandir}/man3/dngettext.3*
%{_mingw32_mandir}/man3/gettext.3*
%{_mingw32_mandir}/man3/ngettext.3*
%{_mingw32_mandir}/man3/textdomain.3*


%changelog
* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-5
- Rename mingw -> mingw32.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-4
- Disable emacs lisp file install

* Thu Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-3
- Remove static libraries.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-2
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
