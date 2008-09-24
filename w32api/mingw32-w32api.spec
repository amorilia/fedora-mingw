%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-w32api
Version:	3.11
Release:        7%{?dist}
Summary:        MinGW Windows cross-compiler Win32 header files

License:        Public Domain
Group:          Development/Libraries
URL:            http://www.mingw.org/
Source0:        http://dl.sourceforge.net/sourceforge/mingw/w32api-%{version}-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-runtime

Requires:       mingw32-filesystem >= 23
Requires:       mingw32-binutils
Requires:       mingw32-gcc
Requires:       mingw32-runtime

# Once this is installed, mingw32-bootstrap (binary bootstrapper) is no
# longer needed.
Obsoletes:      mingw32-w32api-bootstrap
Obsoletes:      mingw-w32api-bootstrap

Provides:       mingw-w32api = %{version}-%{release}
Obsoletes:      mingw-w32api < 3.11-7


%description
MinGW Windows cross-compiler Win32 header files.


%prep
%setup -q -n w32api-%{version}

%build
./configure \
  --build=%_build \
  --host=%{_mingw32_host}

make


%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{_mingw32_prefix} install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_includedir}/*
%{_mingw32_libdir}/*.a


%changelog
* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-7
- Rename mingw -> mingw32.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-6
- Moved ole provides to mingw-filesystem package.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-3
- Use the RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-2
- Initial RPM release, largely based on earlier work from several sources.
