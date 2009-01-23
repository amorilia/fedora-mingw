%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-boost
Version:        1.34.1
Release:        3%{?dist}
Summary:        MinGW Windows port of Boost C++ Libraries

License:        Boost
Group:          Development/Libraries
URL:            http://www.boost.org/
Source0:        http://downloads.sourceforge.net/boost/boost_1_34_1.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         boost-configure.patch
Patch1:         boost-gcc-soname.patch
#Patch2:         boost-use-rpm-optflags.patch
Patch3:         boost-run-tests.patch
Patch4:         boost-regex.patch
Patch5:         boost-gcc43.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 30
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
#BuildRequires:  mingw-libstdc++
BuildRequires:  mingw32-bzip2
BuildRequires:  mingw32-zlib
# These are required by the native package:
#BuildRequires:  mingw32-python
#BuildRequires:  mingw32-libicu


%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been proposed for inclusion in the C++
Standards Committee's upcoming C++ Standard Library Technical Report.)


%prep
%setup -q -n boost_1_34_1
%patch0 -p0
%patch1 -p0
#%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p1


%build
BOOST_ROOT=`pwd`
staged_dir=stage
export BOOST_ROOT

# build make tools, ie bjam, necessary for building libs, docs, and testing
(cd tools/jam/src && ./build.sh)
BJAM=`find tools/jam/src/ -name bjam -a -type f`

#BUILD_FLAGS="--with-toolset=gcc --prefix=$RPM_BUILD_ROOT%{_prefix}"
BUILD_FLAGS="--with-toolset=gcc --with-bjam=$BJAM"
#PYTHON_VERSION=$(python -c 'import sys; print sys.version[:3]')
#PYTHON_FLAGS="--with-python-root=/usr --with-python-version=$PYTHON_VERSION"
PYTHON_FLAGS="--without-libraries=python"
#REGEX_FLAGS="--with-icu"
REGEX_FLAGS="--without-icu"

./configure $BUILD_FLAGS $PYTHON_FLAGS $REGEX_FLAGS

# Make it use the cross-compiler instead of gcc.
rm user-config.jam
echo "using gcc : : %{_mingw32_cc} : ;" > user-config.jam

make %{?_smp_mflags} all


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}

# Boost doesn't build shared libraries for some reason.  However it
# builds *.a files which we can trivially convert to *.dll (they
# contain objects which are already compiled for PIC).
function a2dll
{
  rm -rf .a2dll
  mkdir .a2dll
  pushd .a2dll
  ar x ../$1
  error=0
  i686-pc-mingw32-gcc -shared \
    -o ../$2.dll \
    -Wl,--out-implib,../$2.dll.a \
    *.o -lbz2 -lz -lstdc++ || error=1
  popd
  rm -rf .a2dll
  return $error
}

for f in `find bin.v2 -name '*.a'`; do
  b=`basename $f .a`
  d=`dirname $f`
  if a2dll $f $d/$b; then
    install $d/$b.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
    install $d/$b.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}
  else
    echo '*** FAILED TO BUILD' $d/$b.dll
  fi
done

# install include files
find boost -type d | while read a; do
  mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}/$a
  find $a -mindepth 1 -maxdepth 1 -type f \
    | xargs -r install -m 644 -p -t $RPM_BUILD_ROOT%{_mingw32_includedir}/$a
done

# remove scripts used to generate include files
find $RPM_BUILD_ROOT%{_mingw32_includedir}/ \( -name '*.pl' -o -name '*.sh' \) -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_includedir}/boost
%{_mingw32_bindir}/libboost_date_time.dll
%{_mingw32_libdir}/libboost_date_time.dll.a
%{_mingw32_bindir}/libboost_date_time-mt.dll
%{_mingw32_libdir}/libboost_date_time-mt.dll.a
%{_mingw32_bindir}/libboost_filesystem.dll
%{_mingw32_libdir}/libboost_filesystem.dll.a
%{_mingw32_bindir}/libboost_filesystem-mt.dll
%{_mingw32_libdir}/libboost_filesystem-mt.dll.a
%{_mingw32_bindir}/libboost_graph.dll
%{_mingw32_libdir}/libboost_graph.dll.a
%{_mingw32_bindir}/libboost_graph-mt.dll
%{_mingw32_libdir}/libboost_graph-mt.dll.a
%{_mingw32_bindir}/libboost_iostreams.dll
%{_mingw32_libdir}/libboost_iostreams.dll.a
%{_mingw32_bindir}/libboost_iostreams-mt.dll
%{_mingw32_libdir}/libboost_iostreams-mt.dll.a
%{_mingw32_bindir}/libboost_program_options.dll
%{_mingw32_libdir}/libboost_program_options.dll.a
%{_mingw32_bindir}/libboost_program_options-mt.dll
%{_mingw32_libdir}/libboost_program_options-mt.dll.a
%{_mingw32_bindir}/libboost_regex.dll
%{_mingw32_libdir}/libboost_regex.dll.a
%{_mingw32_bindir}/libboost_regex-mt.dll
%{_mingw32_libdir}/libboost_regex-mt.dll.a
%{_mingw32_bindir}/libboost_serialization.dll
%{_mingw32_libdir}/libboost_serialization.dll.a
%{_mingw32_bindir}/libboost_serialization-mt.dll
%{_mingw32_libdir}/libboost_serialization-mt.dll.a
%{_mingw32_bindir}/libboost_signals.dll
%{_mingw32_libdir}/libboost_signals.dll.a
%{_mingw32_bindir}/libboost_signals-mt.dll
%{_mingw32_libdir}/libboost_signals-mt.dll.a
%{_mingw32_bindir}/libboost_wave.dll
%{_mingw32_libdir}/libboost_wave.dll.a
%{_mingw32_bindir}/libboost_wave-mt.dll
%{_mingw32_libdir}/libboost_wave-mt.dll.a
# These fail to build: they depend on linking with other parts of boost.
#libboost_prg_exec_monitor.dll
#libboost_test_exec_monitor.dll
#libboost_unit_test_framework.dll
#libboost_unit_test_framework-mt.dll
#libboost_test_exec_monitor-mt.dll
#libboost_prg_exec_monitor-mt.dll
#libboost_wserialization.dll
#libboost_wserialization-mt.dll
#libboost_thread-mt.dll


%changelog
* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.34.1-3
- Use _smp_mflags.

* Sat Oct 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.34.1-2
- Initial RPM release.
