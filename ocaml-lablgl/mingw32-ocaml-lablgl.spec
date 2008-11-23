%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-lablgl
Version:        1.03
Release:        1%{?dist}
Summary:        MinGW Windows port of LablGL is an OpenGL interface

License:        BSD
Group:          Development/Libraries

URL:            http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source0:        http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgl-%{version}.tar.gz

# Patches from native Fedora package:
Patch0:         lablgl-tk8.5.patch

Patch1000:      mingw32-ocaml-lablgl-1.03-make-fixes.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-ocaml >= 3.11.0

# labltk is used by the native package, but is essentially optional.
#BuildRequires: mingw32-ocaml-labtk


%description
LablGL is is an Objective Caml interface to OpenGL. Support is
included for use inside LablTk, and LablGTK also includes specific
support for LablGL.  It can be used either with proprietary OpenGL
implementations (SGI, Digital Unix, Solaris...), with XFree86 GLX
extension, or with open-source Mesa.

This is the MinGW Windows port of this package.  Currently it does not
support Togl (Tk integration) or GLUT.


%prep
%setup -q -n lablgl-%{version}

%patch0 -p1
%patch1000 -p1

cat > Makefile.config <<__EOF__
CAMLC = %{_mingw32_target}-ocamlc
CAMLOPT = %{_mingw32_target}-ocamlopt
BINDIR = %{_bindir}
#XINCLUDES = -I%{_prefix}/X11R6/include
#XLIBS = -lXext -lXmu -lX11
#TKINCLUDES = -I%{_includedir}
GLINCLUDES = -DHAS_GLEXT_H -DGL_GLEXT_PROTOTYPES -DGLU_VERSION_1_3
GLLIBS = -lglu32 -lopengl32
GLUTLIBS = -lglut32
RANLIB = i686-pc-mingw32-ranlib
TOOLCHAIN = msvc
XB = .bat
XE = .exe
XS = .dll
# NB: The next two lines have a space after them.
MKLIB = i686-pc-mingw32-ar rcs 
MKDLL = i686-pc-mingw32-ocamlmklib -o 
LIBDIR = %{_libdir}/%{_mingw32_target}-ocaml
DLLDIR = %{_libdir}/%{_mingw32_target}-ocaml/stublibs
INSTALLDIR = %{_libdir}/%{_mingw32_target}-ocaml/lablGL
#TOGLDIR=Togl
#COPTS = $RPM_OPT_FLAGS
__EOF__


%build
make lib
make libopt


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablGL
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/stublibs
make INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablGL \
    DLLDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/stublibs \
    BINDIR=$RPM_BUILD_ROOT%{_bindir} \
    install

# Make and install a META file.
cat <<EOM >META
version="%{version}"
directory="+lablgl"
archive(byte) = "lablgl.cma"
archive(native) = "lablgl.cmxa"
EOM
cp META $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablGL

# Remove unnecessary *.ml files (ones which have a *.mli).
pushd $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablGL
for f in *.ml; do \
  b=`basename $f .ml`; \
  if [ -f "$b.mli" ]; then \
    rm $f; \
  fi; \
done
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/%{_mingw32_target}-ocaml/lablGL/


%changelog
* Sun Nov 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.03-1
- Initial RPM release.
