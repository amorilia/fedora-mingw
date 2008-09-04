%include /usr/lib/rpm/mingw-defs

Name:           mingw-libgcrypt
Version:        1.4.1
Release:        3%{?dist}
Summary:        MinGW Windows gcrypt encryption library

License:        LGPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnupg.org/gcrypt/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 19
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error


%description
MinGW Windows gcrypt encryption library.


%prep
%setup -q -n libgcrypt-%{version}


%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/dumpsexp.exe
%{_mingw_bindir}/libgcrypt-11.dll
%{_mingw_bindir}/libgcrypt-config
%{_mingw_libdir}/libgcrypt.a
%{_mingw_libdir}/libgcrypt.def
%{_mingw_libdir}/libgcrypt.dll.a
%{_mingw_libdir}/libgcrypt.la
%{_mingw_includedir}/gcrypt-module.h
%{_mingw_includedir}/gcrypt.h
%{_mingw_datadir}/aclocal/libgcrypt.m4
%{_mingw_datadir}/info/gcrypt.info

%changelog
* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-3
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.4.1-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-1
- Initial RPM release, largely based on earlier work from several sources.
