# NB: Not for a Fedora package, just an example to show how
# to build Inkscape using the cross-compiler.

%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-inkscape
Version:        20081027
Release:        1%{?dist}
Summary:        MinGW Windows port of Inkscape vector graphics editor

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.inkscape.org/
# Checked out of SVN on the date shown and then just rolled up into
# a tarball.
# svn co https://inkscape.svn.sourceforge.net/svnroot/inkscape/inkscape/trunk inkscape
# tar zcf /tmp/inkscape-%{version}.tar.gz inkscape
Source0:        inkscape-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Source patches needed.
Patch0:         mingw32-inkscape-20081027-no-gc-version-check-when-crosscompiling.patch
Patch1:         mingw32-inkscape-20081027-no-is-os-vista.patch
Patch2:         mingw32-inkscape-20081027-extra-win32-objects.patch
Patch3:         mingw32-inkscape-20081027-pango-enable-engine.patch

# This is a hack, but for some reason PKG_CHECK_MODULES isn't
# updating CFLAGS correctly.  This just works around the problem.
Patch4:         mingw32-inkscape-20081027-Makefile.am-cflags.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-glibmm24
BuildRequires:  mingw32-cairomm
BuildRequires:  mingw32-pangomm
BuildRequires:  mingw32-gtkmm24
BuildRequires:  mingw32-popt
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-libxslt
BuildRequires:  mingw32-gc
BuildRequires:  mingw32-gsl
BuildRequires:  mingw32-boost
BuildRequires:  mingw32-libsigc++20

BuildRequires:  autoconf, automake, libtool
BuildRequires:  perl


%description
An Open Source vector graphics editor, with capabilities similar to
Illustrator, CorelDraw, or Xara X, using the W3C standard Scalable
Vector Graphics (SVG) file format.

Inkscape supports many advanced SVG features (markers, clones, alpha
blending, etc.) and great care is taken in designing a streamlined
interface. It is very easy to edit nodes, perform complex path
operations, trace bitmaps and much more. We also aim to maintain a
thriving user and developer community by using open,
community-oriented development.


%prep
%setup -q -n inkscape

%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

./autogen.sh


%build
%{_mingw32_configure} \
  --enable-lcms=no \
  --without-gnome-vfs

# Additionally remove -lX* libraries from the Makefile.
perl -pi.bak -e 's/-lX\w+//g' src/Makefile

make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/foo.dll
%{_mingw32_libdir}/foo.dll.a
# etc.


%changelog
* Wed Sep 24 2008 Your Name <you@example.com> - 1.2.3-1
- Initial RPM release.
