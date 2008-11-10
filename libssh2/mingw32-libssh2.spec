%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-libssh2
Version:        0.18
Release:        1%{?dist}
Summary:        MinGW Windows library implementing the SSH2 protocol

License:        BSD
Group:          Development/Libraries
URL:            http://www.libssh2.org/
Source0:        http://downloads.sourceforge.net/libssh2/libssh2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-openssl
BuildRequires:  mingw32-zlib
BuildRequires:  autoconf, automake, libtool
BuildRequires:  pkgconfig

# MinGW-specific patches.
# Sent upstream 2008-11-10.
Patch1001:      libssh2-01-build-win-library.patch
Patch1002:      libssh2-02-libssh_priv-headers.patch
Patch1003:      libssh2-03-remove-extra-config.patch
Patch1004:      libssh2-04-non-blocking-examples.patch
Patch1005:      libssh2-05-remove-WINSOCK-VERSION.patch


%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).


%prep
%setup -q -n libssh2-%{version}

%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1

autoreconf


%build
%{_mingw32_configure} --disable-static --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove man pages which duplicate native Fedora.
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}/man3


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/libssh2-1.dll
%{_mingw32_libdir}/libssh2.dll.a
%{_mingw32_libdir}/libssh2.la
%{_mingw32_includedir}/libssh2.h
%{_mingw32_includedir}/libssh2_publickey.h
%{_mingw32_includedir}/libssh2_sftp.h


%changelog
* Mon Nov 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.18-1
- Initial RPM release.
