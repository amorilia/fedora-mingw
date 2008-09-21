%define __strip %{_mingw_strip}
%define __objdump %{_mingw_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw_findrequires}
%define __find_provides %{_mingw_findprovides}

Name:           mingw-gdb
Version:        6.8
Release:        2%{?dist}
Summary:        MinGW port of the GNU debugger (gdb)

License:        GPLv2+
Group:          Development/Libraries
URL:            http://www.mingw.org/MinGWiki/index.php/gdb
Source0:        http://dl.sourceforge.net/sourceforge/mingw/gdb-%{version}-mingw-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         mingw-gdb-6.8-no-getcwd-error.patch

BuildRequires:  mingw-filesystem >= 23
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
PKG_CONFIG_PATH="%{_mingw_libdir}/pkgconfig" \
CC="%{_mingw_cc}" \
CFLAGS=`echo %{_mingw_cflags}` \
./configure \
  --build=%_build --host=%{_mingw_host} --target=%{_mingw_target} \
  --prefix=%{_mingw_prefix} \
  --infodir=%{_mingw_datadir}/info \
  --mandir=%{_mingw_mandir}

make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/gdb.exe
%{_mingw_bindir}/gdbserver.exe
%{_mingw_libdir}/libbfd.a
%{_mingw_libdir}/libbfd.la
%{_mingw_libdir}/libiberty.a
%{_mingw_libdir}/libopcodes.a
%{_mingw_libdir}/libopcodes.la
%{_mingw_includedir}/*
%{_mingw_datadir}/info/*
%{_mingw_mandir}/man1/*.1*
%{_mingw_datadir}/locale/*/LC_MESSAGES/*


%changelog
* Fri Sep 12 2008 Richard W.M. Jones <rjones@redhat.com> - 6.8-2
- Initial RPM release.
