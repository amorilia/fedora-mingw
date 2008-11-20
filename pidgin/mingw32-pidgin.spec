%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-pidgin
Version:        2.5.2
Release:        1%{?dist}
Summary:        MinGW Windows port of Pidgin (ne Gaim)

License:        GPLv2+
Group:          Development/Libraries
URL:            http://www.pidgin.im/
Source0:        http://downloads.sourceforge.net/pidgin/pidgin-2.5.2.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 33
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils


%description
Pidgin is an instant messaging program for Windows, Linux, BSD, and
other Unixes. You can talk to your friends using AIM, ICQ,
Jabber/XMPP, MSN Messenger, Yahoo!, Bonjour, Gadu-Gadu, IRC, Novell
GroupWise Messenger, QQ, Lotus Sametime, SILC, SIMPLE, MySpaceIM, and
Zephyr.

Pidgin can log in to multiple accounts on multiple IM networks
simultaneously. This means that you can be chatting with friends on
AIM, talking to a friend on Yahoo Messenger, and sitting in an IRC
channel all at the same time.


%prep
%setup -q


%build
%{_mingw32_configure}
make


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
* Wed Sep 24 2008 Your Name <you@example.com> - 1.2.3-1
- Initial RPM release.
