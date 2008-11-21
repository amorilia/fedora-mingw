%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-runtime
Version:        3.15.1
Release:        6%{?dist}
Summary:        MinGW Windows cross-compiler runtime and root filesystem

License:        Public Domain
Group:          Development/Libraries
URL:            http://www.mingw.org/
Source0:        http://dl.sourceforge.net/sourceforge/mingw/mingwrt-%{version}-mingw32-src.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 37
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gcc

Requires:       mingw32-binutils
Requires:       mingw32-gcc

# Once this is installed, mingw32-bootstrap (binary bootstrapper) is no
# longer needed.
Obsoletes:      mingw32-runtime-bootstrap


%description
MinGW Windows cross-compiler runtime, base libraries.


%prep
%setup -q -n mingwrt-%{version}-mingw32


%build
MINGW_CFLAGS="%{_mingw32_cflags} -I%{_mingw32_includedir}"
%{_mingw32_configure}
%{_mingw32_make}


%install
rm -rf $RPM_BUILD_ROOT

%{_mingw32_makeinstall}

# make install places these in nonstandard locations, so move them.
mkdir -p $RPM_BUILD_ROOT%{_mingw32_docdir}
mv $RPM_BUILD_ROOT%{_mingw32_prefix}/doc/* $RPM_BUILD_ROOT%{_mingw32_docdir}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/*
%{_mingw32_docdir}/*
%{_mingw32_includedir}/*
%{_mingw32_libdir}/*
%{_mingw32_mandir}/man3/*


%changelog
* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-6
- Remove obsoletes for a long dead package.
- Reenable (and fix) _mingw32_configure (Levente Farkas).

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-5
- Don't use _mingw32_configure macro - doesn't work here.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-4
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-3
- Remove the useconds patch, which is no longer needed (Levente Farkas).
- Use _mingw32_configure macro.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-2
- Rebuild against mingw32-filesystem 36

* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-1
- New upstream version 3.15.1.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-6
- Rename mingw -> mingw32.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-4
- Use RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-2
- Initial RPM release, largely based on earlier work from several sources.
