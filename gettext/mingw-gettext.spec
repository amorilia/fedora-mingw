%include /usr/lib/rpm/mingw-defs

Name:      mingw-gettext
Version:   0.17
Release:   2%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/gettext/
Source0:   http://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires: mingw-gcc
BuildRequires: mingw-gcc-c++
BuildRequires: mingw-binutils
BuildRequires: mingw-iconv


%description
MinGW Windows Gettext library

%prep
%setup -q -n gettext-%{version}

%build
%{_mingw_configure} \
  --disable-java \
  --disable-native-java \
  --disable-csharp \
  --enable-threads=win32

make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_mingw_datadir}/locale/locale.alias
rm -f $RPM_BUILD_ROOT%{_mingw_libdir}/charset.alias
rm -f $RPM_BUILD_ROOT%{_mingw_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_mingw_bindir}/autopoint
%{_mingw_bindir}/envsubst.exe
%{_mingw_bindir}/gettext.exe
%{_mingw_bindir}/gettext.sh
%{_mingw_bindir}/gettextize
%{_mingw_bindir}/libasprintf-0.dll
%{_mingw_bindir}/libgettextlib-0-17.dll
%{_mingw_bindir}/libgettextpo-0.dll
%{_mingw_bindir}/libgettextsrc-0-17.dll
%{_mingw_bindir}/libintl-8.dll
%{_mingw_bindir}/msg*.exe
%{_mingw_bindir}/ngettext.exe
%{_mingw_bindir}/recode-sr-latin.exe
%{_mingw_bindir}/xgettext.exe

%{_mingw_includedir}/autosprintf.h
%{_mingw_includedir}/gettext-po.h
%{_mingw_includedir}/libintl.h

%{_mingw_libdir}/gettext

%{_mingw_libdir}/libasprintf.a
%{_mingw_libdir}/libasprintf.dll.a
%{_mingw_libdir}/libasprintf.la

%{_mingw_libdir}/libgettextlib.dll.a
%{_mingw_libdir}/libgettextlib.la

%{_mingw_libdir}/libgettextpo.a
%{_mingw_libdir}/libgettextpo.dll.a
%{_mingw_libdir}/libgettextpo.la

%{_mingw_libdir}/libgettextsrc.dll.a
%{_mingw_libdir}/libgettextsrc.la

%{_mingw_libdir}/libintl.a
%{_mingw_libdir}/libintl.dll.a
%{_mingw_libdir}/libintl.la

%{_mingw_docdir}/gettext
%{_mingw_docdir}/libasprintf/autosprintf_all.html

%{_mingw_datadir}/emacs/site-lisp/*

%{_mingw_datadir}/gettext/

%{_mingw_datadir}/aclocal/*m4
%{_mingw_datadir}/info/autosprintf.info
%{_mingw_datadir}/info/gettext.info

%{_mingw_datadir}/locale/*/LC_MESSAGES/gettext-tools.mo
%{_mingw_datadir}/locale/*/LC_MESSAGES/gettext-runtime.mo

%{_mingw_mandir}/man1/autopoint.1*
%{_mingw_mandir}/man1/envsubst.1*
%{_mingw_mandir}/man1/gettext.1*
%{_mingw_mandir}/man1/gettextize.1*
%{_mingw_mandir}/man1/msg*1*
%{_mingw_mandir}/man1/ngettext.1*
%{_mingw_mandir}/man1/recode-sr-latin.1*
%{_mingw_mandir}/man1/xgettext.1*

%{_mingw_mandir}/man3/bind_textdomain_codeset.3*
%{_mingw_mandir}/man3/bindtextdomain.3*
%{_mingw_mandir}/man3/dcgettext.3*
%{_mingw_mandir}/man3/dcngettext.3*
%{_mingw_mandir}/man3/dgettext.3*
%{_mingw_mandir}/man3/dngettext.3*
%{_mingw_mandir}/man3/gettext.3*
%{_mingw_mandir}/man3/ngettext.3*
%{_mingw_mandir}/man3/textdomain.3*


%changelog
* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.17-2
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
