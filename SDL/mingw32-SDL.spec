%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-SDL
Version:        1.2.13
Release:        3%{?dist}
Summary:        MinGW Windows port of SDL cross-platform multimedia library

License:        LGPLv2+
Group:          Development/Libraries
URL:            http://www.libsdl.org/
Source0:        http://www.libsdl.org/release/SDL-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

# Patches from native version.
Patch0:         SDL-1.2.10-byteorder.patch
Patch17:        SDL-1.2.13-libdir.patch
Patch21:        SDL-1.2.12-multilib.patch
Patch23:        SDL-1.2.11-dynamic-esd.patch
Patch24:        SDL-1.2.12-x11dyn64.patch
Patch25:        SDL-1.2.12-disable_yasm.patch
Patch26:        SDL-1.2.13-dynamic-pulse.patch
Patch27:        SDL-1.2.13-pulse-rework.patch
Patch28:        SDL-1.2.13-audiodriver.patch

BuildRequires:  mingw32-filesystem >= 40
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-iconv

Requires:       pkgconfig

# Not required at the moment, but SDL does contain plenty of C++ code,
# I just haven't worked out how to enable it.
#BuildRequires:  mingw32-gcc-c++

# If we have nasm in the future, then this would enable future
# optimizations on x86-based architectures.
#%ifarch %{ix86}
#BuildRequires: nasm
#%endif


%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio
device.


%prep
%setup -q -n SDL-%{version}
%patch0 -p1 -b .byteorder
%patch17 -p1 -b .libdir
%patch21 -p1 -b .multilib
%patch23 -p1 -b .dynamic-esd
%patch24 -p1 -b .x11dyn64
%patch25 -p1 -b .disable_yasm
%patch26 -p1 -b .dynamic-pulse
%patch27 -p1 -b .pulse-rework
%patch28 -p1 -b .audiodriver


%build
%{_mingw32_configure} \
  --disable-video-svga --disable-video-ggi --disable-video-aalib \
  --disable-debug \
  --enable-sdl-dlopen \
  --enable-dlopen \
  --enable-arts-shared \
  --enable-esd-shared \
  --enable-pulseaudio-shared \
  --enable-alsa \
  --disable-rpath

make


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libSDL.a

# Actually libSDLmain.a seems to be required.  It just contains
# a single object file called SDL_win32_main.o.
#rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libSDLmain.a

# Delete man pages since they duplicate what is already available
# in base Fedora package.
rm $RPM_BUILD_ROOT%{_mingw32_mandir}/man3/*.3*


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING
%{_mingw32_bindir}/SDL.dll
%{_mingw32_bindir}/sdl-config
%{_mingw32_libdir}/libSDL.dll.a
%{_mingw32_libdir}/libSDL.la
%{_mingw32_libdir}/libSDLmain.a
%{_mingw32_libdir}/pkgconfig/sdl.pc
%{_mingw32_datadir}/aclocal/sdl.m4
%{_mingw32_includedir}/SDL


%changelog
* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.13-3
- Verify we are still up to date with Fedora release.
- Include COPYING in documentation.
- Build with dlfcn.
- List all BRs.
- No need to package the man pages, don't duplicate what's in the
  base Fedora package already.
- Requires pkgconfig.

* Fri Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.13-2
- Initial RPM release.
