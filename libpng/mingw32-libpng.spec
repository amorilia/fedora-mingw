%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libpng
Version:        1.2.34
Release:        2%{?dist}
Summary:        MinGW Windows Libpng library

License:        zlib
URL:            http://www.libpng.org/pub/png/
Source0:        ftp://ftp.simplesystems.org/pub/png/src/libpng-%{version}.tar.bz2
Patch0:         libpng-multilib.patch
Patch1:         libpng-pngconf.patch

Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-zlib

Requires:       pkgconfig

%description
MinGW Windows Libpng library.


%prep
%setup -q -n libpng-%{version}
%patch0 -p1
%patch1 -p1

%build
%{_mingw32_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libpng.a

# No need to distribute manpages which appear in the Fedora
# native packages already.
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc ANNOUNCE CHANGES KNOWNBUG LICENSE README TODO Y2KINFO
%{_mingw32_bindir}/libpng-3.dll
%{_mingw32_bindir}/libpng-config
%{_mingw32_bindir}/libpng12-0.dll
%{_mingw32_bindir}/libpng12-config
%{_mingw32_includedir}/libpng12
%{_mingw32_includedir}/png.h
%{_mingw32_includedir}/pngconf.h
%{_mingw32_libdir}/libpng.dll.a
%{_mingw32_libdir}/libpng.la
%{_mingw32_libdir}/libpng12.a
%{_mingw32_libdir}/libpng12.dll.a
%{_mingw32_libdir}/libpng12.la
%{_mingw32_libdir}/pkgconfig/libpng.pc
%{_mingw32_libdir}/pkgconfig/libpng12.pc


%changelog
* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.34-2
- Depend on mingw32-filesystem >= 40 so we can still build in F-10.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.34-1
- Rebase to 1.2.34 and patches from Fedora.
- Requires pkgconfig.
- Add documentation.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-5
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.2.31-4
- Add patches from rawhide RPM

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-3
- Don't duplicate Fedora native manpages.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.31-2
- Remove static library.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.2.31-1
- Initial RPM release
