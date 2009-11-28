%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# Set to bcond_without or use --with bootstrap if bootstrapping a new release
# or architecture
%bcond_with bootstrap
# Set to bcond_with or use --without gui to disable qt4 gui build
%bcond_without gui
# Set to RC version if building RC, else %{nil}
%define rcver %{nil}

Name:           mingw32-cmake
Version:        2.6.4
Release:        1%{?dist}
Summary:        Cross-platform make system

Group:          Development/Tools
License:        BSD
URL:            http://www.cmake.org
Source0:        http://www.cmake.org/files/v2.6/cmake-%{version}%{rcver}.tar.gz
Source2:        macros.cmake
#Find UseVTK.cmake in /usr/lib64/vtk-* on 64-bit machines
#http://public.kitware.com/mantis/view.php?id=9105
Patch0:         cmake-2.6.4-vtk64.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 23
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
# we use cmake to cross compile the cmake windows binary :-)
BuildRequires: cmake
# Any additional BuildRequires.
#BuildRequires:  ncurses-devel, libX11-devel
#BuildRequires:  curl-devel, expat-devel, zlib-devel
#%if %{without bootstrap}
#BuildRequires: xmlrpc-c-devel
#%endif
#%if %{with gui}
#BuildRequires: qt4-devel, desktop-file-utils
#%define qt_gui --qt-gui
#%endif
#Requires:       rpm


%description
CMake is used to control the software compilation process using simple 
platform and compiler independent configuration files. CMake generates 
native makefiles and workspaces that can be used in the compiler 
environment of your choice. CMake is quite sophisticated: it is possible 
to support complex environments requiring system configuration, pre-processor 
generation, code generation, and template instantiation.


%package        gui
Summary:        Qt GUI for %{name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    gui
The %{name}-gui package contains the Qt based GUI for CMake.


%prep
%setup -q -n cmake-%{version}%{rcver}
%patch0 -p1 -b .vtk64
# Fixup permissions
find -name \*.h -o -name \*.cxx -print0 | xargs -0 chmod -x


%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%{_mingw32_cmake}
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT/%{_mingw32_datadir}/%{name}/Modules -type f | xargs chmod -x
mkdir -p $RPM_BUILD_ROOT%{_mingw32_datadir}/emacs/site-lisp
cp -a Example $RPM_BUILD_ROOT%{_mingw32_datadir}/doc/%{name}-%{version}/
install -m 0644 Docs/cmake-mode.el $RPM_BUILD_ROOT%{_mingw32_datadir}/emacs/site-lisp/
# RPM macros
install -p -m0644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/rpm/macros.cmake
sed -i -e "s|@@CMAKE_VERSION@@|%{version}|" $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/rpm/macros.cmake
touch -r %{SOURCE2} $RPM_BUILD_ROOT%{_mingw32_sysconfdir}/rpm/macros.cmake

#%if %{with gui}
## Desktop file
#desktop-file-install --delete-original \
#  --dir=%{buildroot}%{_datadir}/applications \
#  %{buildroot}/%{_datadir}/applications/CMake.desktop
#%endif


#%check
#unset DISPLAY
#bin/ctest -V

# Remove static libraries but DON'T remove *.dll.a files.
rm $RPM_BUILD_ROOT%{mingw32_libdir}/libfoo.a


%clean
rm -rf $RPM_BUILD_ROOT


#%if %{with gui}
#%post gui
#update-desktop-database &> /dev/null || :
#update-mime-database %{_datadir}/mime &> /dev/null || :

#%postun gui
#update-desktop-database &> /dev/null || :
#update-mime-database %{_datadir}/mime &> /dev/null || :
#%endif


%files
%defattr(-,root,root,-)
%config(noreplace) %{_mingw32_sysconfdir}/rpm/macros.cmake
%{_mingw32_datadir}/doc/%{name}-%{version}/
%{_mingw32_bindir}/ccmake.exe
%{_mingw32_bindir}/cmake.exe
%{_mingw32_bindir}/cpack.exe
%{_mingw32_bindir}/ctest.exe
%{_mingw32_datadir}/%{name}/
%{_mingw32_mandir}/man1/*.1*
%{_mingw32_datadir}/emacs/

%if %{with gui}
%files gui
%defattr(-,root,root,-)
%{_mingw32_bindir}/cmake-gui.exe
%{_mingw32_datadir}/applications/CMake.desktop
%{_mingw32_datadir}/mime/packages/cmakecache.xml
%{_mingw32_datadir}/pixmaps/CMakeSetup.png
%endif


%changelog
* Wed Oct 7 2009 Amorilia <amorilia@users.sourceforge.net> - 2.6.4-1
- Initial RPM release.

