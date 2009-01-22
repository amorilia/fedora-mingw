%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libgpg-error
Version:        1.6
Release:        9%{?dist}
Summary:        MinGW Windows GnuPGP error library

License:        LGPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnupg.org/gcrypt/libgpg-error/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-%{version}.tar.bz2
Source1:        ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-%{version}.tar.bz2.sig
Source2:        wk@g10code.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 27
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-iconv
BuildRequires:  mingw32-gettext

BuildRequires:  gettext


%description
MinGW Windows GnuPGP error library.


%prep
%setup -q -n libgpg-error-%{version}


%build
%{_mingw32_configure}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libgpg-error.a

%find_lang libgpg-error

%clean
rm -rf $RPM_BUILD_ROOT


%files -f libgpg-error.lang
%defattr(-,root,root)
%{_mingw32_bindir}/gpg-error-config
%{_mingw32_bindir}/gpg-error.exe
%{_mingw32_bindir}/libgpg-error-0.dll
%{_mingw32_libdir}/libgpg-error.dll.a
%{_mingw32_libdir}/libgpg-error.la
%{_mingw32_includedir}/gpg-error.h
%{_mingw32_datadir}/aclocal/gpg-error.m4
%{_mingw32_datadir}/common-lisp/source/gpg-error/*

%changelog
* Thu Jan 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.6-9
- Verify that we are still matching current native package.
- Use auto-buildrequires to identify more accurate list of BRs:
    + BR gettext (for /usr/bin/msgfmt etc)
    + BR mingw32-dlfcn
    + BR mingw32-iconv
- Use _smp_mflags.
- Use find_lang.

* Mon Sep 22 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-8
- Rename mingw -> mingw32.
- Depends on mingw-filesystem 27.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.6-6
- Added signature source file & correct URLs

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-5
- Remove static libraries.

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 1.6-4
- Add gettext support

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-3
- Use mingw-filesystem RPM macros.
- BuildArch is noarch.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.6-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- Initial RPM release, largely based on earlier work from several sources.
