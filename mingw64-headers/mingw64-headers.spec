# SVN repo: https://mingw-w64.svn.sourceforge.net/svnroot/mingw-w64
# svn co https://....
# tar zcf mingw-w64-headers-%{svn_revision}.tar.gz \
#   mingw-w64/trunk/mingw-w64-headers
%define svn_revision 607

Name:           mingw64-headers
Version:	0.1
Release:        0.svn%{svn_revision}.6%{?dist}
Summary:        Win32 header files and stubs

License:        Public Domain and LGPLv2+
Group:          Development/Libraries

URL:            http://mingw-w64.sourceforge.net/
Source0:        mingw-w64-headers-%{svn_revision}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw64-filesystem >= 6

Requires:       mingw64-filesystem >= 6


%description
MinGW Windows cross-compiler Win64 header files.


%prep
%setup -q -n mingw-w64

find -name .svn | xargs rm -r
find -name ChangeLog -delete

# There are a few other odd *.c and *.dlg files amongst the
# headers.  Should we delete them?  (XXX)


%build
# nothing


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw64_includedir}

cp -a trunk/mingw-w64-headers/include/* $RPM_BUILD_ROOT%{_mingw64_includedir}/
cp -a trunk/mingw-w64-headers/direct-x/include/* $RPM_BUILD_ROOT%{_mingw64_includedir}/

# XXX We don't know why this is required, but gcc/cc1 fails
# to find the header files without it.
pushd $RPM_BUILD_ROOT%{_mingw64_exec_prefix}
ln -s include include64
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw64_includedir}/*
%{_mingw64_exec_prefix}/include64


%changelog
* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.svn607.6
- Started mingw64 development.

* Mon Dec 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.13-1
- New upstream version 3.13.

* Tue Dec  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-8
- Force rebuild to get rid of the binary bootstrap package and replace
  with package built from source.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-7
- No runtime dependency on binutils or gcc.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-6
- Rebuild against latest filesystem package.
- Rewrite the summary for accuracy and brevity.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-4
- Remove obsoletes for a long dead package.
- Enable _mingw32_configure (Levente Farkas).

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-3
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-2
- Rebuild against mingw32-filesystem 36

* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-1
- New upstream version 3.12.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-7
- Rename mingw -> mingw32.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-6
- Moved ole provides to mingw-filesystem package.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-3
- Use the RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-2
- Initial RPM release, largely based on earlier work from several sources.
