%define debug_package %{nil}

Name:           darwinx-filesystem
Version:        2
Release:        1%{?dist}
Summary:        Darwin-cross base filesystem and environment

License:        GPLv2+
Group:          Development/Libraries

URL:            http://hg.et.redhat.com/misc/fedora-mingw--devel/
Source0:        COPYING

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       setup
Requires:       rpm


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora Darwin (Mac OS X) cross-compiler packages.


%prep
%setup -q -c -T

cp %{SOURCE0} COPYING


%build
# nothing


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/powerpc-apple-darwin7/include

for arch in powerpc i386; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/bin
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/include
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/lib
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/lib/pkgconfig
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/share
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/share/aclocal
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/share/doc
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/share/info
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/share/man
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/share/man/man{1,2,3,4,5,6,7,8,l,n}
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING
%{_prefix}/i386-apple-darwin8/
%{_prefix}/powerpc-apple-darwin7/
%{_prefix}/powerpc-apple-darwin8/


%changelog
* Sun Feb  8 2009 Richard W.M. Jones <rjones@redhat.com> - 2-1
- Initial RPM release.
