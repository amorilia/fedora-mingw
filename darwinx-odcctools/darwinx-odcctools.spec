# Note about the source for these tools:
#
# Apple distributes a set of tools called cctools under the APSL2.0
# license.  You can get it from
# http://www.opensource.apple.com/darwinsource/Current/
# but you will need an Apple ID (although it's still open source).
#
# These are the OpenDarwin odcctools, which are an enhanced version of
# an older version of these tools.  However OpenDarwin and odcctools
# appears to be dead, replaced first by DarwinPorts, but even that
# hasn't seen a release for more than 2 years.
#
# Nevertheless, this is odcctools, until I can work out what is the
# right upstream we should be using.
#
# The version number is based on the original cctools from which this
# odcctools was derived.

%define odcc_version 590.36
%define odcc_stamp 20060413

Name:           darwinx-odcctools
Version:        %{odcc_version}
Release:        0.%{odcc_stamp}.4%{?dist}
Summary:        Darwin (Mac OS X) cross-compiler tools

License:        APSL 2.0
Group:          Development/Libraries

URL:            http://odcctools.darwinports.com/
Source0:        odcctools-%{odcc_stamp}.tar.bz2

Patch1:         odcctools-headers.patch
Patch2:         odcctools-lp64.patch
Patch3:         odcctools-x86-64.patch
Patch4:         odcctools-ofile.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  darwinx-filesystem >= 1

BuildRequires:  elfutils, kernel-headers, libstdc++-devel

Requires:       darwinx-filesystem >= 1


%description
The odcctools project is geared towards improving the Darwin
cctools build system and code base to support Darwin development.


%prep
%setup -q -n odcctools-%{odcc_stamp}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1


%build
for arch in powerpc i386; do
  mkdir build-$arch
  pushd build-$arch

  ../configure \
    --target=$arch-apple-darwin8 \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --datadir=%{_datadir} \
    --mandir=%{_mandir} \
    --libexecdir=%{_libexecdir}

  make %{?_smp_mflags}

  popd
done

%install
rm -rf $RPM_BUILD_ROOT

for arch in powerpc i386; do
  make -C build-$arch DESTDIR=$RPM_BUILD_ROOT install
done

# Rename the manual pages so they don't conflict with the
# ones for the native tools.
for f in $RPM_BUILD_ROOT%{_mandir}/*/*; do
  d=$(dirname $f); b=$(basename $f)
  mv $f $d/i386-apple-darwin8-$b
  ln $d/i386-apple-darwin8-$b $d/powerpc-apple-darwin8-$b
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc APPLE_LICENSE
%{_bindir}/i386-apple-darwin8-*
%{_bindir}/powerpc-apple-darwin8-*
%{_includedir}/mach-o/
%{_libexecdir}/as/
%{_libdir}/libmacho.a
%{_mandir}/man1/i386-apple-darwin8-*.1*
%{_mandir}/man1/powerpc-apple-darwin8-*.1*
%{_mandir}/man3/i386-apple-darwin8-*.3*
%{_mandir}/man3/powerpc-apple-darwin8-*.3*
%{_mandir}/man5/i386-apple-darwin8-*.5*
%{_mandir}/man5/powerpc-apple-darwin8-*.5*


%changelog
* Sun Feb  8 2009 Richard W.M. Jones <rjones@redhat.com> - 590.36-0.20060413.4
- Initial RPM release for Fedora.

* Tue Mar 28 2006 Benjamin Reed <rangerrick@befunk.com> - 590.36-1
- fixed build to just use srcdir != builddir, changed to 10.3/10.4-specific

* Sun Feb 26 2006 Benjamin Reed <rangerrick@befunk.com> - 590.23.2od12-1
- initial release
