%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-gdb
Version:        6.8
Release:        4%{?dist}
Summary:        MinGW port of the GNU debugger (gdb)

License:        GPLv2+
Group:          Development/Libraries
URL:            http://www.mingw.org/MinGWiki/index.php/gdb
Source0:        http://dl.sourceforge.net/sourceforge/mingw/gdb-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         mingw32-gdb-6.8-no-getcwd-error.patch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  flex


%description
This is the MinGW port of the GNU debugger (gdb).

Note this is a Fedora native binary which debugs Windows target
executables.


%prep
%setup -q -n gdb-%{version}
%patch0 -p1


%build
# Using echo normalizes spaces between the flags.
PKG_CONFIG_PATH="%{_mingw32_libdir}/pkgconfig" \
CC="%{_mingw32_cc}" \
CFLAGS=`echo %{_mingw32_cflags}` \
./configure \
  --build=%_build --host=%{_mingw32_host} --target=%{_mingw32_target} \
  --prefix=%{_mingw32_prefix} \
  --infodir=%{_mingw32_datadir}/info \
  --mandir=%{_mingw32_mandir}

make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/gdb.exe
%{_mingw32_bindir}/gdbserver.exe
%{_mingw32_libdir}/libbfd.a
%{_mingw32_libdir}/libbfd.la
%{_mingw32_libdir}/libiberty.a
%{_mingw32_libdir}/libopcodes.a
%{_mingw32_libdir}/libopcodes.la
%{_mingw32_includedir}/*
%{_mingw32_datadir}/info/*
%{_mingw32_mandir}/man1/*.1*
%{_mingw32_datadir}/locale/*/LC_MESSAGES/*


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 6.8-4
- Rebuild for mingw32-gcc 4.4

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 6.8-3
- Rename mingw -> mingw32.

* Fri Sep 12 2008 Richard W.M. Jones <rjones@redhat.com> - 6.8-2
- Initial RPM release.
