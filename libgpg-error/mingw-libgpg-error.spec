%include /usr/lib/rpm/mingw-defs

Name:           mingw-libgpg-error
Version:        1.6
Release:        5%{?dist}
Summary:        MinGW Windows GnuPGP error library

License:        LGPLv2+
Group:          Development/Libraries
URL:            ftp://ftp.gnupg.org/GnuPG/libgpg-error
Source0:        ftp://ftp.gnupg.org/GnuPG/libgpg-error/libgpg-error-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw-filesystem >= 17
BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-gettext

%description
MinGW Windows GnuPGP error library.


%prep
%setup -q -n libgpg-error-%{version}


%build
%{_mingw_configure}
make


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_mingw_libdir}/libgpg-error.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw_bindir}/gpg-error-config
%{_mingw_bindir}/gpg-error.exe
%{_mingw_bindir}/libgpg-error-0.dll
%{_mingw_libdir}/libgpg-error.dll.a
%{_mingw_libdir}/libgpg-error.la
%{_mingw_includedir}/gpg-error.h
%{_mingw_datadir}/locale/*/LC_MESSAGES/libgpg-error.mo
%{_mingw_datadir}/aclocal/gpg-error.m4
%{_mingw_datadir}/common-lisp/source/gpg-error/*

%changelog
* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-5
- Remove static libraries.

* Fri Sep  5 2008 Daniel P. Berrange <berrange@redhat.com> - 1.6-4
- Add gettext support

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-3
- Use mingw-filesystem RPM macros.
- BuildArch is noarch.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 1.6-2
- List files explicitly and use custom CFLAGS

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- Initial RPM release, largely based on earlier work from several sources.
