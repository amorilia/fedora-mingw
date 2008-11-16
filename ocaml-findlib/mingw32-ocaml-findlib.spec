%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

%define debug_package %{nil}

# Findlib is a build tool, and we don't need to cross-compile it
# (except arguably the findlib library, but no one really uses that).
# However we do need the MinGW-specific META files in the right
# places, and that is what this package contains.
#
# To use ocamlfind with the MinGW META files, do:
#
# OCAMLFIND_CONF=/etc/i686-pc-mingw32-ocamlfind.conf \
#   ocamlfind cmd ...

Name:           mingw32-ocaml-findlib
Version:        1.2.2
Release:        7%{?dist}
Summary:        MinGW Windows Objective CAML package manager and build helper

License:        BSD
Group:          Development/Libraries

URL:            http://projects.camlcity.org/projects/findlib.html
Source0:        http://download.camlcity.org/download/findlib-%{version}.tar.gz
Source1000:     ocamlfind.conf.in

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  ocaml
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-labltk-devel
BuildRequires:  mingw32-ocaml >= 3.11.0+beta1-8
BuildRequires:  m4
BuildRequires:  gawk

# Installing this should pull in ocamlfind (native binary).
Requires:       ocaml-findlib

# Early versions were accidentally misnamed.
Obsoletes:      mingw32-findlib <= 1.2.2-5


%description
Objective CAML package manager and build helper.


%prep
%setup -q -n findlib-%{version}


%build
%{_mingw32_target}-ocamlopt -version
%{_mingw32_target}-ocamlopt -where
(cd tools/extract_args && make)
tools/extract_args/extract_args -o src/findlib/ocaml_args.ml \
  %{_mingw32_target}-ocamlc \
  %{_mingw32_target}-ocamlcp \
  %{_mingw32_target}-ocamlmktop \
  %{_mingw32_target}-ocamlopt \
  %{_mingw32_target}-ocamldep \
  %{_mingw32_target}-ocamldoc ||:
cat src/findlib/ocaml_args.ml
./configure -config %{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf \
  -bindir %{_bindir} \
  -sitelib `%{_mingw32_target}-ocamlopt -where` \
  -mandir %{_mandir} \
  -with-toolbox
make all
make opt
rm doc/guide-html/TIMESTAMP



%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml

make install prefix=$RPM_BUILD_ROOT OCAMLFIND_BIN=$RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT/$RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_bindir}

# Remove documentation which is already available
# in the Fedora native package.
rm -r $RPM_BUILD_ROOT%{_mandir}/man[15]/

# Remove ocamlfind binary - we will use the native version.
rm $RPM_BUILD_ROOT%{_bindir}/ocamlfind
rm $RPM_BUILD_ROOT%{_bindir}/safe_camlp4

# Remove findlib & num-top libs: if anything uses these we can
# add them back later.
rm -r $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/findlib
rm -r $RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml/num-top

# XXX topfind gets installed as %{_libdir}/ocaml - not sure why
# but delete it anyway.
rm $RPM_BUILD_ROOT%{_libdir}/ocaml

# Override /etc/%{_mingw32_target}-ocamlfind.conf with our
# own version.
rm $RPM_BUILD_ROOT%{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf
sed \
  -e 's,@libdir@,%{_libdir},g' \
  -e 's,@target@,%{_mingw32_target},g' \
  < %{SOURCE1000} \
  > $RPM_BUILD_ROOT%{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%config %{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf
%{_libdir}/%{_mingw32_target}-ocaml/bigarray/META
%{_libdir}/%{_mingw32_target}-ocaml/camlp4/META
%{_libdir}/%{_mingw32_target}-ocaml/dbm/META
%{_libdir}/%{_mingw32_target}-ocaml/dynlink/META
%{_libdir}/%{_mingw32_target}-ocaml/graphics/META
%{_libdir}/%{_mingw32_target}-ocaml/labltk/META
%{_libdir}/%{_mingw32_target}-ocaml/num/META
%{_libdir}/%{_mingw32_target}-ocaml/stdlib/META
%{_libdir}/%{_mingw32_target}-ocaml/str/META
%{_libdir}/%{_mingw32_target}-ocaml/threads/META
%{_libdir}/%{_mingw32_target}-ocaml/unix/META


%changelog
* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-7
- Use ocamlc now that we have it.
- Rename package correctly.
- Pull in ocamlfind binary.

* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-3
- Initial RPM release.
