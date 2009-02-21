# Note about the source for these tools:
#
# Apple distributes a set of tools called cctools under the APSL2.0
# license.  You can get it from
# http://www.opensource.apple.com/darwinsource/Current/
# but you will need an Apple ID (although it's still open source).
#
# These are the OpenDarwin odcctools, which are an enhanced version of
# an older version of cctools.
#
# OpenDarwin is dead.  It was replaced first by DarwinPorts, which has
# not released anything for more than two years.
#
# There are various other potential upstreams for these tools.  Most
# promising is: http://code.google.com/p/iphone-dev/
#
#   odcctools version    based on cctools    source
#   -----------------------------------------------------------
#   20060413             590.36              OpenDarwin (dead)
#   20061117             ?                       ""
#   20070629             ?                   Shipped by Gentoo
#   up to 2008           622.3 or 667.8.0    Google code: iphone-dev
#
# odcctools DOES NOT compile on 64 bit platforms.  The code contains
# fundamental 32 bit assumptions, for example that the return value
# from calloc can fit into a 32 bit integer.  Therefore on 64 bit
# platforms we have to compile with 'gcc -m32'.

%define odcc_version 590.36
%define odcc_stamp 20060413

Name:           darwinx-odcctools
Version:        %{odcc_version}
Release:        0.%{odcc_stamp}.6%{?dist}
Summary:        Darwin (Mac OS X) cross-compiler tools

License:        APSL 2.0
Group:          Development/Libraries

URL:            http://odcctools.darwinports.com/
Source0:        odcctools-%{odcc_stamp}.tar.bz2

Patch1:         odcctools-headers.patch
Patch2:         odcctools-ofile.patch

# These two patches were an attempt to get the code to compile
# on 64 bit architectures.  However the 32 bit assumptions in the
# code run much deeper than this.
#Patch3:         odcctools-lp64.patch
#Patch4:         odcctools-x86-64.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  darwinx-filesystem >= 1

BuildRequires:  elfutils, kernel-headers, libstdc++-devel

# Temporary hack for smock on x86_64.
BuildRequires:  /usr/include/gnu/stubs-32.h
BuildRequires:  /usr/lib/gcc/i586-redhat-linux

Requires:       darwinx-filesystem >= 1


%description
The odcctools project is geared towards improving the Darwin
cctools build system and code base to support Darwin development.


%prep
%setup -q -n odcctools-%{odcc_stamp}

%patch1 -p1
%patch2 -p1

#%patch3 -p1
#%patch4 -p1


%build
for arch in powerpc i386; do
  mkdir build-$arch
  pushd build-$arch

#%if %{__isa_bits} 64  <-- how to write this with RPM? XXX
  CFLAGS="-m32" LDFLAGS="-m32" \
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
* Sat Feb 21 2009 Richard W.M. Jones <rjones@redhat.com> - 590.36-0.20060413.6
- Fedora Rawhide now uses 'i586' as arch for 32-bit gcc.

* Sun Feb 15 2009 Richard W.M. Jones <rjones@redhat.com> - 590.36-0.20060413.5
- Build as a 32 bit binary.
- Add note about upstream versions.

* Sun Feb  8 2009 Richard W.M. Jones <rjones@redhat.com> - 590.36-0.20060413.4
- Initial RPM release for Fedora.

* Tue Mar 28 2006 Benjamin Reed <rangerrick@befunk.com> - 590.36-1
- fixed build to just use srcdir != builddir, changed to 10.3/10.4-specific

* Sun Feb 26 2006 Benjamin Reed <rangerrick@befunk.com> - 590.23.2od12-1
- initial release
