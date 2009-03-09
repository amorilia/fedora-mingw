%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-jasper
Version:        1.900.1
Release:        8%{?dist}
Summary:        MinGW Windows Jasper library

License:        JasPer
Group:          Development/Libraries

URL:            http://www.ece.uvic.ca/~mdadams/jasper/
Source0:        http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-%{version}.zip

# Patches from Fedora native package.
# OpenGL is disabled in this build, so we don't need this patch:
#Patch1:         jasper-1.701.0-GL.patch
# Note patch2 appears in native package, but is not applied:
#Patch2:         jasper-1.701.0-GL-ac.patch
Patch3:         patch-libjasper-stepsizes-overflow.diff

# MinGW-specific patches.
# This patch adds '-no-undefined' flag to libtool line:
Patch1000:      jasper-1.900.1-mingw32.patch
# This patch is a bit of a hack, but it's just there to fix a demo program:
Patch1001:      jasper-1.900.1-sleep.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-libjpeg
BuildRequires:  mingw32-dlfcn


%description
MinGW Windows Jasper library.


%prep
%setup -q -n jasper-%{version}
%patch3 -p1 -b .CVE-2007-2721

%patch1000 -p1 -b .mingw32
%patch1001 -p1 -b .sleep


%build
%{_mingw32_configure} \
  --disable-opengl --enable-libjpeg --disable-static --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install mandir=%{_mingw32_mandir}

# Remove the manual pages - don't duplicate documentation which
# is in the native Fedora package.
rm $RPM_BUILD_ROOT%{_mingw32_mandir}/man1/*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYRIGHT LICENSE NEWS README
%{_mingw32_bindir}/i686-pc-mingw32-imgcmp.exe
%{_mingw32_bindir}/i686-pc-mingw32-imginfo.exe
%{_mingw32_bindir}/i686-pc-mingw32-jasper.exe
%{_mingw32_bindir}/i686-pc-mingw32-tmrdemo.exe
%{_mingw32_bindir}/libjasper-1.dll
%{_mingw32_libdir}/libjasper.dll.a
%{_mingw32_libdir}/libjasper.la
%{_mingw32_includedir}/jasper/


%changelog
* Mon Mar  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-8
- Fix defattr line.
- Remove the enable-shared patch, and just use --enable-shared on
  the configure line.
- Disable the GL patch since OpenGL is disabled.
- Document what the patches are for in the spec file.
- Only patch Makefile.in so we don't have to rerun autotools, and
  remove autotools dependency.

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-7
- Rebuild for mingw32-gcc 4.4

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-6
- Use _smp_mflags.
- Disable static libraries.
- Include documentation.
- Use the same patches as Fedora native package.
- Just run autoconf instead of autoreconf so we don't upgrade libtool.
- +BR mingw32-dlfcn.
- Don't need the manual pages.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-5
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-4
- Add overflow patch from rawhide

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-3
- Run autoreconf after changing configure.ac script and add BRs for autotools

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.900.1-2
- Enable DLLs.
- Remove static libraries.

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 1.900.1-1
- Initial RPM release
