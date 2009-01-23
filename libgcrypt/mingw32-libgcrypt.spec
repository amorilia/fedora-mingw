%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libgcrypt
Version:        1.4.3
Release:        3%{?dist}
Summary:        MinGW Windows gcrypt encryption library

License:        LGPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnupg.org/gcrypt/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
Source1:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2.sig
Source2:        wk@g10code.com
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libgpg-error


%description
MinGW Windows gcrypt encryption library.


%prep
%setup -q -n libgcrypt-%{version}


%build
PATH="%{_mingw32_bindir}:$PATH" \
%{_mingw32_configure} --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

# Remove info pages which duplicate what is in Fedora natively.
rm -rf $RPM_BUILD_ROOT%{_mingw32_infodir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/dumpsexp.exe
%{_mingw32_bindir}/hmac256.exe
%{_mingw32_bindir}/libgcrypt-11.dll
%{_mingw32_bindir}/libgcrypt-config
%{_mingw32_libdir}/libgcrypt.def
%{_mingw32_libdir}/libgcrypt.dll.a
%{_mingw32_libdir}/libgcrypt.la
%{_mingw32_includedir}/gcrypt-module.h
%{_mingw32_includedir}/gcrypt.h
%{_mingw32_datadir}/aclocal/libgcrypt.m4


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.4.3-3
- Use _smp_mflags.
- Disable static libraries.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.3-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.3-1
- Update to 1.4.3 release

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-6
- Remove info pages.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-5
- Set PATH so it finds gpg-error-config

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-4
- Remove static library.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-3
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
