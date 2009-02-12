Name:           mingw64-binutils
Version:        2.19.1
Release:        4%{?dist}
Summary:        MinGW Windows binutils

License:        GPLv2+ and LGPLv2+ and GPLv3+ and LGPLv3+
Group:          Development/Libraries

URL:            http://www.gnu.org/software/binutils/
Source0:        http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.bz2

# Possible patch added after 2.19.1:
# http://sourceware.org/ml/binutils/2009-02/msg00090.html

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  texinfo
BuildRequires:  mingw64-filesystem >= 6

# NB: This must be left in.
Requires:       mingw64-filesystem >= 6


%description
MinGW Windows binutils (utilities like 'strip', 'as', 'ld') which
understand Windows executables and DLLs.


%prep
%setup -q -n binutils-%{version}


%build
mkdir -p build
cd build
CFLAGS="$RPM_OPT_FLAGS" \
../configure \
  --build=%_build --host=%_host \
  --target=%{_mingw64_target} \
  --verbose --disable-nls \
  --without-included-gettext \
  --disable-win32-registry \
  --disable-werror \
  --with-sysroot=%{_mingw64_sysroot} \
  --prefix=%{_prefix} --bindir=%{_bindir} \
  --includedir=%{_includedir} --libdir=%{_libdir} \
  --mandir=%{_mandir} --infodir=%{_infodir}

make %{?_smp_mflags} all


%install
rm -rf $RPM_BUILD_ROOT

cd build
make DESTDIR=$RPM_BUILD_ROOT install

# These files conflict with ordinary binutils.
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libiberty*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mandir}/man1/*
%{_bindir}/x86_64-pc-mingw32-*
%{_prefix}/x86_64-pc-mingw32/bin
%{_prefix}/x86_64-pc-mingw32/lib/ldscripts


%changelog
* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-4
- Started mingw64 development.

* Tue Feb 10 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.1-1
- New upstream version 2.19.1.

* Mon Dec 15 2008 Richard W.M. Jones <rjones@redhat.com> - 2.19-1
- New upstream version 2.19.

* Sat Nov 29 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-10
- Must runtime-require mingw32-filesystem.

* Fri Nov 21 2008 Levente Farkas <lfarkas@lfarkas.org> - 2.18.50_20080109_2-9
- BR mingw32-filesystem >= 38

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-8
- Rename mingw -> mingw32.
- BR mingw32-filesystem >= 26.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-7
- Use mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.50_20080109_2-5
- Initial RPM release, largely based on earlier work from several sources.
