%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-ocaml-libvirt
Version:        0.4.4.2
Release:        1%{?dist}
Summary:        MinGW Windows port of OCaml binding for libvirt

License:        LGPLv2+
Group:          Development/Libraries

URL:            http://libvirt.org/ocaml/
Source0:        http://libvirt.org/sources/ocaml/ocaml-libvirt-%{version}.tar.gz

Patch1000:      mingw32-ocaml-libvirt-0.4.4.2-build.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 35
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-ocaml >= 3.11.0+beta1-13
BuildRequires:  mingw32-libvirt >= 0.2.1
BuildRequires:  perl
BuildRequires:  gawk
BuildRequires:  autoconf, automake, libtool


%description
OCaml binding for libvirt.


%prep
%setup -q -n ocaml-libvirt-%{version}

%patch1000 -p1

autoreconf


%build
export OCAMLFIND_CONF=%{_sysconfdir}/%{_mingw32_target}-ocamlfind.conf
%{_mingw32_configure}
make OCAMLMKLIB=%{_mingw32_target}-ocamlmklib opt


%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_CONF=/etc/i686-pc-mingw32-ocamlfind.conf
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/%{_mingw32_target}-ocaml

mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs

#make install-opt
pushd libvirt
ocamlfind install -ldconf ignore libvirt ../META *.a *.cmx *.cmxa *.cmi *.mli
popd
pushd mlvirsh
make install-opt
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/mlvirsh
%{_libdir}/%{_mingw32_target}-ocaml/libvirt/


%changelog
* Sun Nov 16 2008 Richard W.M. Jones <rjones@redhat.com> - 0.4.4.2-1
- Initial RPM release.
