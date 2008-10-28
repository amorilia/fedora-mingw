# NB: Not for a Fedora package, just an example to show how
# to build Inkscape using the cross-compiler.

%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-inkscape
Version:        20081027
Release:        5%{?dist}
Summary:        MinGW Windows port of Inkscape vector graphics editor

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.inkscape.org/

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Checked out of SVN on the date shown and then just rolled up into
# a tarball.
# svn co https://inkscape.svn.sourceforge.net/svnroot/inkscape/inkscape/trunk inkscape
# tar zcf /tmp/inkscape-%{version}.tar.gz inkscape
Source0:        inkscape-%{version}.tar.gz

# Rolled-up source patch, submitted upstream on 2008-10-27.
Patch0:         mingw32-inkscape-20081027.patch

# Fix the paths.
Patch1:         mingw32-inkscape-20081027-paths.patch

# This patch is only needed to run under Wine, which doesn't
# supported getting the outline of unhinted fonts.
Patch2:         /mingw32-inkscape-20081027-unhinted-fonts-for-wine.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-fontconfig
BuildRequires:  mingw32-freetype
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

BuildRequires:  autoconf, automake, libtool, intltool

# For /usr/bin/glib-gettextize
BuildRequires:  glib2-devel


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

./autogen.sh


%build
PATH=%{_mingw32_bindir}:$PATH \
%{_mingw32_configure} \
  --enable-lcms=no \
  --without-gnome-vfs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/inkscape.exe
%{_mingw32_bindir}/inkview.exe
%{_mingw32_datadir}/applications/inkscape.desktop
%{_mingw32_datadir}/inkscape/
%{_mingw32_datadir}/locale/*/LC_MESSAGES/inkscape.mo
%{_mingw32_datadir}/pixmaps/inkscape.png
%{_mingw32_mandir}/*/man1/*.1
%{_mingw32_mandir}/man1/*.1


%changelog
* Mon Oct 27 2008 Richard W.M. Jones <rjones@redhat.com> - 20081027-5
- Initial RPM release.
