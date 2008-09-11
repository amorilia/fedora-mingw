Name:           mingw-gdb
Version:        6.8
Release:        1%{?dist}
Summary:        MinGW port of the GNU debugger (gdb)

License:        GPLv2+
Group:          Development/Libraries
URL:            http://www.mingw.org/MinGWiki/index.php/gdb
Source0:        http://dl.sourceforge.net/sourceforge/mingw/gdb-%{version}-mingw-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         mingw-gdb-6.8-no-getcwd-error.patch

BuildRequires:  mingw-filesystem >= 23
BuildRequires:  flex
BuildRequires:  chrpath

Requires:       mingw-filesystem >= 23
Requires:       mingw-binutils
Requires:       mingw-runtime


%description
This is the MinGW port of the GNU debugger (gdb).

Note this is a Fedora native binary which debugs Windows target
executables.


%prep
%setup -q -n gdb-%{version}
%patch0 -p1


%build
CC="%{__cc} ${RPM_OPT_FLAGS}" \
./configure \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --includedir=%{_includedir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --infodir=%{_infodir} \
  --datadir=%{_datadir} \
  --build=%_build --host=%_host \
  --target=%{_mingw_target}
make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove files that clash with other installed stuff.
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a
rm -rf $RPM_BUILD_ROOT%{_infodir}/*
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale

# Remove rpaths
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_bindir}/i686-pc-mingw32-gdb
%{_bindir}/i686-pc-mingw32-gdbtui
%{_mandir}/man1/*.1*


%changelog
* Thu Sep 11 2008 Richard W.M. Jones <rjones@redhat.com> - 6.8-1
- Initial RPM release.
