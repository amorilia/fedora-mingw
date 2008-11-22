%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-sqlite
Version:        3.5.9
Release:        3%{?dist}
Summary:        MinGW Windows port of sqlite embeddable SQL database engine

License:        Public Domain
Group:          Applications/Databases
URL:            http://www.sqlite.org/
Source0:        http://www.sqlite.org/sqlite-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

Patch1:         sqlite-3.5.8-pkgconfig-version.patch

Patch1000:      mingw32-sqlite-3.5.9-no-undefined.patch

BuildRequires:  mingw32-filesystem >= 26
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-pdcurses
BuildRequires:  mingw32-readline
BuildRequires:  mingw32-termcap >= 1.3.1-3

BuildRequires:  autoconf
BuildRequires:  libtool


%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

This package contains cross-compiled libraries and development tools
for Windows.


%prep
%setup -q -n sqlite-%{version}
%patch1 -p1
%patch1000 -p1

# Ships with an old/broken version of libtool which cannot create
# Windows libraries properly.  So pull in the current version.
autoreconf
libtoolize --force


%build
# I think there's a bug in the configure script where, if
# cross-compiling, it cannot correctly determine the target executable
# extension (ie. .exe).  As a result it doesn't correctly detect that
# the target is Windows and so tries to use Unix-specific functions
# which don't exist.  In any case we can work around this by forcing
# the extension via this export.
#   - RWMJ 2008-09-30
export config_TARGET_EXEEXT=.exe

%{_mingw32_configure}
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libsqlite3.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/sqlite3.exe
%{_mingw32_bindir}/libsqlite3-0.dll
%{_mingw32_libdir}/libsqlite3.dll.a
%{_mingw32_libdir}/libsqlite3.la
%{_mingw32_includedir}/sqlite3.h
%{_mingw32_includedir}/sqlite3ext.h
%{_mingw32_libdir}/pkgconfig/sqlite3.pc
# etc.


%changelog
* Sat Nov 22 2008 Richard Jones <rjones@redhat.com> - 3.5.9-3
- Rebuild against new readline.

* Fri Oct 31 2008 Richard Jones <rjones@redhat.com> - 3.5.9-2
- Rebuild against latest termcap.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 3.5.9-1
- Initial RPM release.
