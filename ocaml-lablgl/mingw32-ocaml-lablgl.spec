%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-example
Version:        1.03
Release:        1%{?dist}
Summary:        MinGW Windows port of LablGL is an OpenGL interface

License:        BSD
Group:          Development/Libraries

URL:            http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source0:        http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgl-%{version}.tar.gz

# Patches from native Fedora package:
Patch0:         lablgl-tk8.5.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw32-ocaml

# XXX This requires camlp4 which we don't yet have under MinGW.
BuildRequires:  mingw32-ocaml-camlp4

# labltk is used by the native package, but is essentially optional.
#BuildRequires: mingw32-ocaml-labtk


%description
LablGL is is an Objective Caml interface to OpenGL. Support is
included for use inside LablTk, and LablGTK also includes specific
support for LablGL.  It can be used either with proprietary OpenGL
implementations (SGI, Digital Unix, Solaris...), with XFree86 GLX
extension, or with open-source Mesa.


%prep
%setup -q -n lablgl-%{version}

%patch0 -p1

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
MKLIB = ar rcs
MKDLL = i686-pc-mingw32-gcc -shared -o
LIBDIR = %{_libdir}/%{_mingw32_target}-ocaml
DLLDIR = %{_libdir}/%{_mingw32_target}-ocaml/stublibs
INSTALLDIR = %{_libdir}/%{_mingw32_target}-ocaml/lablGL
#TOGLDIR=Togl
#COPTS = $RPM_OPT_FLAGS
__EOF__


%build
make all opt


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
* Thu Nov 13 2008 Your Name <you@example.com> - 1.2.3-1
- Initial RPM release.
