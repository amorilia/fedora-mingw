%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

# For versioning, please see the native Fedora package.
%define alphatag 20020319

Name:           mingw32-ocaml-curses
Version:        0.1
Release:        4%{?dist}
Summary:        MinGW Windows OCaml bindings for ncurses

License:        LGPLv2+
Group:          Development/Libraries

URL:            http://savannah.nongnu.org/projects/ocaml-tmk/
Source0:        ocaml-curses-%{alphatag}.tar.gz

# Patches for MinGW:
Patch1000:      mingw32-ocaml-curses-0.1-build.patch
Patch1001:      mingw32-ocaml-curses-0.1-win32-functions.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-ocaml >= 3.11.0+beta1-9
BuildRequires:  mingw32-ocaml-findlib
BuildRequires:  mingw32-pdcurses


%description
OCaml bindings for curses.


%prep
%setup -q -c -n %{name}-%{alphatag}

%patch1000 -p1
%patch1001 -p1


%build
ulimit -s unlimited

cd curses

make \
  OCAMLC=%{_mingw32_target}-ocamlopt \
  OCAMLOPT=%{_mingw32_target}-ocamlopt \
  OCAMLMKLIB=%{_mingw32_target}-ocamlmklib \
  CURSES="" opt

cat > META <<EOF
name = "curses"
version = "%{version}"
description = "OCaml bindings for ncurses"
requires = ""
archive(byte) = "mlcurses.cma"
archive(native) = "mlcurses.cmxa"
EOF


%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_CONF=%{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml

mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
pushd curses
ocamlfind install curses META *.cmi *.cmx *.cmxa *.a *.mli
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_libdir}/%{_mingw32_target}-ocaml/curses/


%changelog
* Mon Nov 17 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-4
- libmlcurses.a contained a copy of pdcurses.dll.a in error.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-3
- Use ocamlfind to install in the correct location.
- Install the META file.
- Fix the version number in changelog.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1-2
- Initial release.
