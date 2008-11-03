%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# We are using 'temporarily' the windbus project, which is a port of
# dbus and dbus-c++ to Windows.  At some point it is expected these
# will be merged back into the main dbus tree.
#
# In Fedora native, dbus and dbus-c++ are separate packages.  Here it
# is convenient to combine them into a single specfile / separate sub-
# packages.

%define date 20081031

Name:           mingw32-dbus
Version:        1.2.4
Release:        0.1.%{date}svn%{?dist}
Summary:        MinGW Windows port of DBus

License:        GPLv2+ or AFL
Group:          Development/Libraries
URL:            http://sourceforge.net/projects/windbus
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# svn co https://windbus.svn.sourceforge.net/svnroot/windbus windbus
# tar zcf windbus-%{version}-%{date}.tar.gz trunk
# tar zcf windbus-c++-%{version}-%{date}.tar.gz dbuscxx
Source0:        windbus-%{version}-%{date}.tar.gz
Source1:        windbus-c++-%{version}-%{date}.tar.gz

# This patch is extremely hacky, and not upstream.
#
# windbus seems to prefer to use cmake to build instead of the
# original dbus autotools.  This patch hacks up the autotools
# files to work instead.  Really instead of just replacing the
# *unix*.c files with *win*.c we ought to include both and add
# proper #ifdef WIN32...#endif around the code.
Patch0:         mingw32-dbus-1.2.4-20081031-mingw32.patch

# This patch is almost, but not quite working.  For some reason
# the implementation of _dbus_poll (from the C library above) cannot
# be accessed by the C++ library.
Patch1:         mingw32-dbus-1.2.4-20081031-c++-mingw32.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-glib2
BuildRequires:  mingw32-gtk2
BuildRequires:  mingw32-gtkmm24
BuildRequires:  mingw32-expat
BuildRequires:  libtool, automake, autoconf

# This keeps dbus-c++ subpackage happy while building.  We have
# hacked the Makefile to give the correct location of the libraries.
BuildRequires:  dbus-devel


%description
D-BUS is a system for sending messages between applications. It is
used both for the systemwide message bus service, and as a
per-user-login-session messaging facility.


%package c++
Summary:        MinGW Windows port of DBus
License:        LGPLv2+
Group:          Development/Libraries

%description c++
Native C++ bindings for D-Bus for use in C++ programs.


%prep
%setup -q -b 0 -c
%setup -q -a 1 -T -D

pushd trunk
%patch0 -p2
autoreconf
chmod +x configure
popd

pushd dbuscxx
%patch1 -p2
autoreconf
popd


%build
pushd trunk
# Avoid a test which fails when cross-compiling:
export ac_cv_have_abstract_sockets=no

# For unknown reasons, the configure script chokes if you
# pass --build explicitly.  We also need to pass -DDBUS_WIN
# as an extra flag.
PKG_CONFIG_PATH="%{_mingw32_libdir}/pkgconfig" \
CC="%{_mingw32_cc}" \
CFLAGS="%{_mingw32_cflags} -DDBUS_WIN -DDBUS_BUILD_TESTS" \
./configure \
  --host=%{_mingw32_host} \
  --target=%{_mingw32_target} \
  --prefix=%{_mingw32_prefix} \
  --with-xml=expat
make
popd

pushd dbuscxx
%{_mingw32_configure}
# XXX Does not quite work yet.
make ||:
popd


%install
rm -rf $RPM_BUILD_ROOT
pushd trunk
make DESTDIR=$RPM_BUILD_ROOT install
popd

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libdbus-1.a

# Remove manpages because they duplicate what's in the
# Fedora native package already.
rm -r $RPM_BUILD_ROOT%{_mingw32_mandir}/man1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/dbus-daemon.exe
%{_mingw32_bindir}/i686-pc-mingw32-dbus-monitor.exe
%{_mingw32_bindir}/i686-pc-mingw32-dbus-send.exe
%{_mingw32_bindir}/libdbus-1-3.dll
%{_mingw32_libdir}/dbus-1.0/
%{_mingw32_libdir}/libdbus-1.dll.a
%{_mingw32_libdir}/libdbus-1.la
%{_mingw32_libdir}/pkgconfig/dbus-1.pc
%{_mingw32_sysconfdir}/dbus-1/
%{_mingw32_sysconfdir}/rc.d/init.d/i686-pc-mingw32-messagebus
%{_mingw32_includedir}/dbus-1.0/



%changelog
* Mon Nov  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-0.1.20081031svn
- Initial RPM release.
