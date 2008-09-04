%include /usr/lib/rpm/mingw-defs

Name:           mingw-runtime
Version:	3.14
Release:        4%{?dist}
Summary:        MinGW Windows cross-compiler runtime and root filesystem

License:        Public Domain
Group:          Development/Libraries
URL:            http://www.mingw.org/
Source0:        http://dl.sourceforge.net/sourceforge/mingw/%{name}-%{version}-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:  mingw-filesystem >= 9
BuildRequires:  mingw-binutils
BuildRequires:  mingw-gcc

Requires:       mingw-filesystem >= 9
Requires:       mingw-binutils
Requires:       mingw-gcc

# Once this is installed, mingw-bootstrap (binary bootstrapper) is no
# longer needed.
Obsoletes:      mingw-bootstrap


%description
MinGW Windows cross-compiler runtime, base libraries.


%prep
%setup -q

%build
CFLAGS="-I%{_mingw_includedir}" \
./configure \
  --build=%_build \
  --host=%{_mingw_host}

make


%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT%{_mingw_prefix} install

# make install places these in nonstandard locations, so move them.
mkdir -p $RPM_BUILD_ROOT%{_mingw_docdir}
mv $RPM_BUILD_ROOT%{_mingw_prefix}/doc/* $RPM_BUILD_ROOT%{_mingw_docdir}/
mkdir -p $RPM_BUILD_ROOT%{_mingw_mandir}
mv $RPM_BUILD_ROOT%{_mingw_prefix}/man/* $RPM_BUILD_ROOT%{_mingw_mandir}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/*
%{_mingw_docdir}/*
%{_mingw_includedir}/*
%{_mingw_libdir}/*
%{_mingw_mandir}/man3/*


%changelog
* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-4
- Use RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-2
- Initial RPM release, largely based on earlier work from several sources.
