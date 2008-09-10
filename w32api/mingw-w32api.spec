%include /usr/lib/rpm/mingw-defs

Name:           mingw-w32api
Version:	3.11
Release:        6%{?dist}
Summary:        MinGW Windows cross-compiler Win32 header files

License:        Public Domain
Group:          Development/Libraries
URL:            http://www.mingw.org/
Source0:        http://dl.sourceforge.net/sourceforge/mingw/w32api-%{version}-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:  mingw-filesystem >= 3
BuildRequires:  mingw-binutils
BuildRequires:  mingw-gcc
BuildRequires:  mingw-runtime

Requires:       mingw-filesystem >= 3
Requires:       mingw-binutils
Requires:       mingw-gcc
Requires:       mingw-runtime

# Once this is installed, mingw-bootstrap (binary bootstrapper) is no
# longer needed.
Obsoletes:      mingw-bootstrap

#%define _use_internal_dependency_generator 0
#%define __debug_install_post %{nil}


%description
MinGW Windows cross-compiler Win32 header files.


%prep
%setup -q -n w32api-%{version}

%build
./configure \
  --build=%_build \
  --host=%{_mingw_host}

make


%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{_mingw_prefix} install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_includedir}/*
%{_mingw_libdir}/*.a


%changelog
* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-6
- Moved ole provides to mingw-filesystem package.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-3
- Use the RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-2
- Initial RPM release, largely based on earlier work from several sources.
