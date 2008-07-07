Name:           mingw-runtime
Version:	3.14
Release:        1%{?dist}
Summary:        MinGW Windows cross-compiler runtime and root filesystem

License:        Public Domain
Group:          Development/Libraries
URL:            http://www.mingw.org/
Source0:        http://dl.sourceforge.net/sourceforge/mingw/%{name}-%{version}-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:  mingw-binutils
BuildRequires:  mingw-gcc

# Once this is installed, mingw-bootstrap (binary bootstrapper) is no
# longer needed.
Obsoletes:      mingw-bootstrap

#%define _use_internal_dependency_generator 0
#%define __debug_install_post %{nil}


%description
MinGW Windows cross-compiler runtime, base libraries and root filesystem.


%prep
%setup -q

%build
./configure \
  --build=%_build \
  --host=i686-pc-mingw32

make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_prefix}/i686-pc-mingw32/lib/libiberty.a
%{_libdir}/gcc/i686-pc-mingw32
%{_libexecdir}/gcc/i686-pc-mingw32
%{_bindir}/i686-pc-mingw32-*
%{_mandir}/man1/i686-pc-mingw32-*


%changelog
* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.1-1
- Initial RPM release, largely based on earlier work from several sources.
