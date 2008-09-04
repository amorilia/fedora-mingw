%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:      mingw-gettext
Version:   0.17
Release:   1%{?dist}
Summary:   GNU libraries and utilities for producing multi-lingual messages

License:   GPLv2+ and LGPLv2+
Group:     Development/Libraries
URL:       http://www.gnu.org/software/gettext/
Source0:   http://ftp.gnu.org/pub/gnu/gettext/gettext-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: mingw-gcc
BuildRequires: mingw-gcc-c++
BuildRequires: mingw-binutils
BuildRequires: mingw-iconv

Requires:       mingw-runtime

%description
MinGW Windows Gettext library

%prep
%setup -q -n gettext-%{version}

%build
CFLAGS="-O2 -g -Wall -pipe" \
./configure \
  --build=%_build \
  --host=i686-pc-mingw32 \
  --prefix=%{_prefix}/i686-pc-mingw32/sys-root/mingw \
  --disable-java \
  --disable-native-java \
  --disable-csharp \
  --enable-threads=win32

make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/locale/locale.alias

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/autopoint
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/envsubst.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gettext.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gettext.sh
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/gettextize
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libasprintf-0.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgettextlib-0-17.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgettextpo-0.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libgettextsrc-0-17.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/libintl-8.dll
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/msg*.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/ngettext.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/recode-sr-latin.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/xgettext.exe

%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/autosprintf.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/gettext-po.h
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/libintl.h

%dir %{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/gettext/
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/gettext/hostname.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/gettext/project-id
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/gettext/urlget.exe
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/gettext/user-email

%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/charset.alias

%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libasprintf.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libasprintf.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libasprintf.la

%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgettextlib.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgettextlib.la

%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgettextpo.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgettextpo.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgettextpo.la

%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgettextsrc.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libgettextsrc.la


%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libintl.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libintl.dll.a
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/libintl.la

%dir %{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc/gettext
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc/gettext/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/doc/libasprintf/*

%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/emacs/site-lisp/*

%dir %{_prefix}/i686-pc-mingw32/sys-root/mingw/share/gettext/
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/gettext/*

%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/*m4
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/autosprintf.info
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/gettext.info

%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/locale/*/LC_MESSAGES/gettext-tools.mo
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/locale/*/LC_MESSAGES/gettext-runtime.mo

%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/autopoint.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/envsubst.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/gettext.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/gettextize.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/msg*1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/ngettext.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/recode-sr-latin.1*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/xgettext.1*

%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/bind_textdomain_codeset.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/bindtextdomain.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/dcgettext.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/dcngettext.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/dgettext.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/dngettext.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/gettext.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/ngettext.3*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/textdomain.3*


%changelog
* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.17-1
- Initial RPM release, largely based on earlier work from several sources.
