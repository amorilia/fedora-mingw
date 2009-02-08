Name:           darwinx-headers
Version:        1.2
Release:        1%{?dist}
Summary:        Darwin (Mac OS X) header files

License:        APSL2.0
Group:          Development/Libraries

URL:            http://www.opensource.apple.com/darwinsource/

# XXX Where is the upstream tarball located?
Source0:        headers-10.3.tar.bz2
Source1:        headers-10.4.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  darwinx-filesystem >= 2

Requires:       darwinx-filesystem >= 2


%description
This package contains system headers for cross-compiling to Darwin
(Mac OS X).


%prep
%setup -q -c -n %{name}
%setup -q -c -n %{name} -b 1


%build
# Nothing.


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}/powerpc-apple-darwin7
cp -a headers-10.3 $RPM_BUILD_ROOT%{_prefix}/powerpc-apple-darwin7/include
ln -sf include $RPM_BUILD_ROOT%{_prefix}/powerpc-apple-darwin7/sys-include

for arch in powerpc i386; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8
  cp -a headers-10.4 $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/include
  ln -sf include $RPM_BUILD_ROOT%{_prefix}/$arch-apple-darwin8/sys-include
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_prefix}/powerpc-apple-darwin7/include/*
%{_prefix}/powerpc-apple-darwin7/sys-include
%{_prefix}/powerpc-apple-darwin8/include/*
%{_prefix}/powerpc-apple-darwin8/sys-include
%{_prefix}/i386-apple-darwin8/include/*
%{_prefix}/i386-apple-darwin8/sys-include


%changelog
* Sun Feb  8 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2-1
- Initial RPM release for Fedora.

* Tue Mar 28 2006 Benjamin Reed <rangerrick@befunk.com> - 1.1-1
- added 10.3 headers, rearranged things a bit

* Sun Feb 26 2006 Benjamin Reed <rangerrick@befunk.com> - 1.0-1
- initial release
