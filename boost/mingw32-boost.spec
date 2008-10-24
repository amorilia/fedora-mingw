%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-boost
Version:        1.34.1
Release:        1%{?dist}
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

make all


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mingw32_includedir}

# install lib
for i in `find stage -type f -name \*.a`; do
  NAME=`basename $i`;
  install -p -m 0644 $i $RPM_BUILD_ROOT%{_mingw32_libdir}/$NAME;
done;
for i in `find stage -type f -name \*.so`; do
  NAME=$i;
  SONAME=$i.3;
  VNAME=$i.%{version};
  base=`basename $i`;
  NAMEbase=$base;
  SONAMEbase=$base.3;
  VNAMEbase=$base.%{version};
  mv $i $VNAME;
  ln -s $VNAMEbase $SONAME;
  ln -s $VNAMEbase $NAME;
  install -p -m 755 $VNAME $RPM_BUILD_ROOT%{_libdir}/$VNAMEbase;
  mv $SONAME $RPM_BUILD_ROOT%{_libdir}/$SONAMEbase;
  mv $NAME $RPM_BUILD_ROOT%{_libdir}/$NAMEbase;
done;

# install include files
find %{name} -type d | while read a; do
  mkdir -p $RPM_BUILD_ROOT%{_includedir}/$a
  find $a -mindepth 1 -maxdepth 1 -type f \
    | xargs -r install -m 644 -p -t $RPM_BUILD_ROOT%{_includedir}/$a
done

# remove scripts used to generate include files
find $RPM_BUILD_ROOT%{_includedir}/ \( -name '*.pl' -o -name '*.sh' \) -exec rm {} \;


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
