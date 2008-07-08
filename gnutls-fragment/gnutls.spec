# XXX This prevents binaries from being stripped.  Using ordinary 'strip'
# on a MinGW library actually corrupts the library, hence we must disable
# this action.  However we would still like Fedora binaries to be stripped.
%define __os_install_post /usr/lib/rpm/brp-compress %{nil}

Summary: A TLS protocol implementation
Name: gnutls
Version: 2.4.1
Release: 2%{?dist}
# The libgnutls library is LGPLv2+, utilities and remaining libraries are GPLv3+
License: GPLv3+ and LGPLv2+
Group: System Environment/Libraries
BuildRequires: libgcrypt-devel >= 1.2.2, gettext
BuildRequires: zlib-devel, readline-devel, libtasn1-devel
BuildRequires: lzo-devel
URL: http://www.gnutls.org/
#Source0: ftp://ftp.gnutls.org/pub/gnutls/devel/%{name}-%{version}.tar.gz
#Source1: ftp://ftp.gnutls.org/pub/gnutls/devel/%{name}-%{version}.tar.gz.sig
# XXX patent tainted SRP code removed.
Source0: %{name}-%{version}-nosrp.tar.bz2
Source1: libgnutls-config
Patch1: gnutls-2.4.0-nosrp.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: libgcrypt >= 1.2.2

%package devel
Summary: Development files for the %{name} package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgcrypt-devel
Requires: pkgconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%package utils
Summary: Command line tools for TLS protocol
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%package -n mingw-gnutls
Summary:        MinGW Windows cross-compile of %{name} package
Group:          Development/Libraries

BuildRequires:  mingw-gcc
BuildRequires:  mingw-binutils
BuildRequires:  mingw-libgpg-error
BuildRequires:  mingw-libgcrypt

Requires:       mingw-runtime
Requires:       mingw-libgpg-error
Requires:       mingw-libgcrypt


%description
GnuTLS is a project that aims to develop a library which provides a secure 
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.

%description devel
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains files needed for developing applications with
the GnuTLS library.

%description utils
GnuTLS is a project that aims to develop a library which provides a secure
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains command line TLS client and server and certificate
manipulation tools.

%description -n mingw-gnutls
GnuTLS is a project that aims to develop a library which provides a secure 
layer, over a reliable transport layer. Currently the GnuTLS library implements
the proposed standards by the IETF's TLS working group.
This package contains a MinGW Windows cross-compiled library so that
you can build programs that depend on GnuTLS library for Windows from
a Fedora host.

%prep
%setup -q
%patch1 -p1 -b .nosrp

for i in auth_srp_rsa.c auth_srp_sb64.c auth_srp_passwd.c auth_srp.c gnutls_srp.c ext_srp.c; do
    touch lib/$i
done

%build
mkdir build
pushd build
echo '../configure "$@"' > configure; chmod +x configure
%configure --with-libtasn1-prefix=%{_prefix} \
           --with-included-libcfg \
           --disable-srp-authentication
make
popd

mkdir i686-pc-mingw32
pushd i686-pc-mingw32
CFLAGS="$RPM_OPT_FLAGS -fno-stack-protector" \
../configure \
  --build=%_build \
  --host=i686-pc-mingw32 \
  --prefix=%{_prefix}/i686-pc-mingw32/sys-root/mingw \
  --disable-cxx \
  --with-included-libtasn1 \
  --with-included-libcfg \
  --disable-srp-authentication
make
popd

%install
rm -fr $RPM_BUILD_ROOT
pushd build
%makeinstall
rm -f $RPM_BUILD_ROOT%{_bindir}/srptool
rm -f $RPM_BUILD_ROOT%{_bindir}/gnutls-srpcrypt
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-config
cp -f %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/libgnutls-extra-config
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/srptool.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man3/*srp*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
%find_lang %{name}
popd

pushd i686-pc-mingw32
make DESTDIR=$RPM_BUILD_ROOT install
popd

%check
pushd build
make check
popd

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/gnutls.info.gz ]; then
    /sbin/install-info %{_infodir}/gnutls.info.gz %{_infodir}/dir || :
fi

%preun devel
if [ $1 = 0 -a -f %{_infodir}/gnutls.info.gz ]; then
   /sbin/install-info --delete %{_infodir}/gnutls.info.gz %{_infodir}/dir || :
fi

%files -f build/%{name}.lang
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%doc COPYING COPYING.LIB README AUTHORS

%files devel
%defattr(-,root,root,-)
%{_bindir}/libgnutls*-config
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_infodir}/gnutls*

%files utils
%defattr(-,root,root,-)
%{_bindir}/certtool
%{_bindir}/psktool
%{_bindir}/gnutls*
%{_mandir}/man1/*

%files -n mingw-gnutls
%defattr(-,root,root)
%{_prefix}/i686-pc-mingw32/sys-root/mingw/bin/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/lib/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/include/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/aclocal/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/info/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man1/*
%{_prefix}/i686-pc-mingw32/sys-root/mingw/share/man/man3/*

%changelog
* Tue Jul  8 2008 Richard W.M. Jones <rjones@redhat.com> 2.4.1-2
- Build mingw-gnutls subpackage.

* Tue Jul  1 2008 Tomas Mraz <tmraz@redhat.com> 2.4.1-1
- new upstream version
- correct the license tag
- explicit --with-included-opencdk not needed
- use external lzo library, internal not included anymore

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> 2.4.0-1
- upgrade to latest upstream

* Tue May 20 2008 Tomas Mraz <tmraz@redhat.com> 2.0.4-3
- fix three security issues in gnutls handshake - GNUTLS-SA-2008-1
  (#447461, #447462, #447463)

* Mon Feb  4 2008 Joe Orton <jorton@redhat.com> 2.0.4-2
- use system libtasn1

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> 2.0.4-1
- upgrade to latest upstream

* Tue Aug 21 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-2
- license tag fix

* Wed Jun  6 2007 Tomas Mraz <tmraz@redhat.com> 1.6.3-1
- upgrade to latest upstream (#232445)

* Tue Apr 10 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-2
- properly require install-info (patch by Ville Skyttä)
- standard buildroot and use dist tag
- add COPYING and README to doc

* Wed Feb  7 2007 Tomas Mraz <tmraz@redhat.com> 1.4.5-1
- new upstream version
- drop libtermcap-devel from buildrequires

* Thu Sep 14 2006 Tomas Mraz <tmraz@redhat.com> 1.4.1-2
- detect forged signatures - CVE-2006-4790 (#206411), patch
  from upstream

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.1-1
- upgrade to new upstream version, only minor changes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.0-1.1
- rebuild

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.0-1
- upgrade to new upstream version (#192070), rebuild
  of dependent packages required

* Tue May 16 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-2
- added missing buildrequires

* Mon Feb 13 2006 Tomas Mraz <tmraz@redhat.com> - 1.2.10-1
- updated to new version (fixes CVE-2006-0645)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.9-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.9-3
- rebuilt

* Fri Dec  9 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-2
- replaced *-config scripts with calls to pkg-config to
  solve multilib conflicts

* Wed Nov 23 2005 Tomas Mraz <tmraz@redhat.com> 1.2.9-1
- upgrade to newest upstream
- removed .la files (#172635)

* Sun Aug  7 2005 Tomas Mraz <tmraz@redhat.com> 1.2.6-1
- upgrade to newest upstream (rebuild of dependencies necessary)

* Mon Jul  4 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-2
- split the command line tools to utils subpackage

* Sat Apr 30 2005 Tomas Mraz <tmraz@redhat.com> 1.0.25-1
- new upstream version fixes potential DOS attack

* Sat Apr 23 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-2
- readd the version script dropped by upstream

* Fri Apr 22 2005 Tomas Mraz <tmraz@redhat.com> 1.0.24-1
- update to the latest upstream version on the 1.0 branch

* Wed Mar  2 2005 Warren Togami <wtogami@redhat.com> 1.0.20-6
- gcc4 rebuild

* Tue Jan  4 2005 Ivana Varekova <varekova@redhat.com> 1.0.20-5
- add gnutls Requires zlib-devel (#144069)

* Mon Nov 08 2004 Colin Walters <walters@redhat.com> 1.0.20-4
- Make gnutls-devel Require libgcrypt-devel

* Tue Sep 21 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-3
- rebuild with release++, otherwise unchanged.

* Tue Sep  7 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-2
- patent tainted SRP code removed.

* Sun Sep  5 2004 Jeff Johnson <jbj@redhat.com> 1.0.20-1
- update to 1.0.20.
- add --with-included-opencdk --with-included-libtasn1
- add --with-included-libcfg --with-included-lzo
- add --disable-srp-authentication.
- do "make check" after build.

* Fri Mar 21 2003 Jeff Johnson <jbj@redhat.com> 0.9.2-1
- upgrade to 0.9.2

* Tue Jun 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.4-1
- update to 0.4.4.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 25 2002 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- update to 0.4.3.

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com> 0.4.2-1
- update to 0.4.2.
- change license to LGPL.
- include splint annotations patch.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.4.0-1
- update to 0.4.0

* Thu Jan 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-1
- update to 0.3.2

* Wed Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 0.3.0-1
- add a URL

* Wed Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
