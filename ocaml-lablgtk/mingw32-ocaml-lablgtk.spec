%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-lablgtk
Version:        2.10.1
Release:        2%{?dist}
Summary:        MinGW Windows port of LablGTK, OCaml interface to Gtk+

License:        LGPLv2 with exceptions
Group:          Development/Libraries

URL:            http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgtk.html
Source0:        http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgtk-%{version}.tar.gz

Patch1000:      mingw32-ocaml-lablgtk-2.10.1-build-hacks.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 38
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-glib2
BuildRequires:  mingw32-gtk2
BuildRequires:  mingw32-pango

BuildRequires:  mingw32-ocaml >= 3.11.0
BuildRequires:  mingw32-ocaml-lablgl >= 1.03

BuildRequires:  pkgconfig

# These are all in the native package, but missing as dependencies.
#BuildRequires:  ncurses-devel
#BuildRequires:  gnome-panel-devel
#BuildRequires:  gtkglarea2-devel
#BuildRequires:  gtkspell-devel
#BuildRequires:  libXmu-devel
#BuildRequires:  libglade2-devel
#BuildRequires:  libgnomecanvas-devel
#BuildRequires:  libgnomeui-devel
#BuildRequires:  librsvg2-devel


%description
LablGTK is is an Objective Caml interface to gtk+.

It uses the rich type system of Objective Caml 3 to provide a strongly
typed, yet very comfortable, object-oriented interface to gtk+. This
is not that easy if you know the dynamic typing approach taken by
gtk+.

This is the MinGW Windows port of this package.  Currently it does not
support Togl (Tk integration).


%prep
%setup -q -n lablgtk-%{version}

%patch1000 -p1

# version information in META file is wrong
perl -pi -e 's|version="1.3.1"|version="%{version}"|' META


%build
%{_mingw32_configure} \
  CAMLC=i686-pc-mingw32-ocamlc \
  OCAMLCDOTOPT=no \
  CAMLOPT=i686-pc-mingw32-ocamlopt \
  OCAMLOPTDOTOPT=no \
  OCAMLDEP=i686-pc-mingw32-ocamldep \
  OCAMLLIB=%{_libdir}/%{_mingw32_target}-ocaml \
  CAMLMKTOP=i686-pc-mingw32-ocamlmktop \
  CAMLMKLIB=i686-pc-mingw32-ocamlmklib \
  EXE=.exe \
  --enable-debug \
  --without-glade \
  --without-rsvg \
  --without-gl \
  --without-gnomecanvas \
  --without-gnomeui \
  --without-panel \
  --without-gtkspell \
  --without-gtksourceview

perl -pi -e "s|-O|$RPM_OPT_FLAGS|" src/Makefile
make world


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablgtk2
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/stublibs

make install \
     BINDIR=$RPM_BUILD_ROOT%{_mingw32_bindir} \
     LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
     INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablgtk2 \
     DLLDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/stublibs
cp META $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablgtk2

# Remove unnecessary *.ml files (ones which have a *.mli).
pushd $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/lablgtk2
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
%{_mingw32_bindir}/lablgtk2
%{_libdir}/%{_mingw32_target}-ocaml/lablgtk2/


%changelog
* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-2
- Rebuild for mingw32-gcc 4.4

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.10.1-1
- Initial RPM release.
