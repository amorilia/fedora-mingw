%define __strip %{_mingw64_strip}
%define __objdump %{_mingw64_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw64_findrequires}
%define __find_provides %{_mingw64_findprovides}

# SVN repo: https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64
# svn co https://....
# tar zcf mingw-w64-headers-%{svn_revision}.tar.gz \
#   mingw-w64/trunk/mingw-w64-headers
%define svn_revision 607

Name:           mingw64-runtime
Version:        0.1
Release:        0.svn%{svn_revision}.1%{?dist}
Summary:        MinGW Windows cross-compiler runtime

License:        Public Domain
Group:          Development/Libraries
URL:            http://mingw-w64.sourceforge.net/
Source0:        mingw-w64-crt-%{svn_revision}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw64-filesystem >= 3
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-gcc-bootstrap


%description
MinGW Windows cross-compiler runtime, base libraries.


%prep
%setup -q -n mingw-w64


%build
pushd trunk/mingw-w64-crt
%{_mingw64_configure} --with-sysroot=%{_mingw64_prefix}
make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT

pushd trunk/mingw-w64-crt
make DESTDIR=$RPM_BUILD_ROOT install
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw64_libdir}/*


%changelog
* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.svn607.1
- Started mingw64 development.

* Tue Feb 10 2009 Richard W.M. Jones <rjones@redhat.com> - 3.15.2-1
- New upstream release 3.15.2.

* Tue Dec  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-10
- Force rebuild to get rid of the binary bootstrap package and replace
  with package built from source.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-9
- No runtime dependency on binutils or gcc.
- But it DOES BR w32api.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-8
- Rebuild against latest filesystem package.
- MINGW_CFLAGS -> MINGW32_CFLAGS.
- Rewrite the summary for accuracy and brevity.

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
