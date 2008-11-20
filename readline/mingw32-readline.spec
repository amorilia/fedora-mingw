%define __strip %{_mingw32_strip}
%define __objdump %{_mingw32_objdump}
%define _use_internal_dependency_generator 0
%define __find_requires %{_mingw32_findrequires}
%define __find_provides %{_mingw32_findprovides}

Name:           mingw32-readline
Version:        5.2
Release:        3%{?dist}
Summary:        MinGW port of readline for editing typed command lines

License:        GPLv2+
Group:          System Environment/Libraries
URL:            http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Source0:        ftp://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1:         readline-5.2-shlib.patch
Patch2:         readline-5.2-001.patch
Patch3:         readline-5.2-002.patch
Patch4:         readline-5.2-003.patch
Patch5:         readline-5.2-004.patch
Patch6:         readline-5.2-005.patch
Patch7:         readline-5.2-006.patch
Patch8:         readline-5.2-007.patch
Patch9:         readline-5.2-008.patch
Patch10:        readline-5.2-009.patch
Patch11:        readline-5.2-010.patch
Patch12:        readline-5.2-011.patch
Patch13:        readline-5.2-redisplay-sigint.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 29
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-termcap >= 1.3.1-3


%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

This is a port of the library and development tools to Windows.


%prep
%setup -q -n readline-%{version}
%patch1 -p1 -b .shlib
%patch2 -p0 -b .001
%patch3 -p0 -b .002
%patch4 -p0 -b .003
%patch5 -p0 -b .004
%patch6 -p0 -b .005
%patch7 -p0 -b .006
%patch8 -p0 -b .007
%patch9 -p0 -b .008
%patch10 -p0 -b .009
%patch11 -p0 -b .010
%patch12 -p0 -b .011
%patch13 -p1 -b .redisplay-sigint

pushd examples
rm -f rlfe/configure
iconv -f iso8859-1 -t utf8 -o rl-fgets.c{_,}
touch -r rl-fgets.c{,_}
mv -f rl-fgets.c{_,}
popd


%build
%{_mingw32_configure} --enable-shared
make SHLIB_LIBS=-ltermcap

# Rebuild the DLLs correctly and create implibs.
pushd shlib
%{_mingw32_cc} -shared -o readline.dll -Wl,--out-implib,readline.dll.a readline.so vi_mode.so funmap.so keymaps.so parens.so search.so rltty.so complete.so bind.so isearch.so display.so signals.so util.so kill.so undo.so macro.so input.so callback.so terminal.so text.so nls.so misc.so xmalloc.so history.so histexpand.so histfile.so histsearch.so shell.so mbutil.so tilde.so compat.so -ltermcap
%{_mingw32_cc} -shared -o history.dll -Wl,--out-implib,history.dll.a history.so histexpand.so histfile.so histsearch.so shell.so mbutil.so xmalloc.so
popd


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Remove the fake .so files and install our DLLs and implibs.
pushd shlib
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/lib*.so.*
mkdir -p $RPM_BUILD_ROOT%{_mingw32_bindir}
install readline.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install readline.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}
install history.dll $RPM_BUILD_ROOT%{_mingw32_bindir}
install history.dll.a $RPM_BUILD_ROOT%{_mingw32_libdir}
popd

# Don't want the info files or manpages which duplicate the native package.
rm -rf $RPM_BUILD_ROOT%{_mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{_mingw32_infodir}

# Don't want the static library.
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libhistory.a
rm $RPM_BUILD_ROOT%{_mingw32_libdir}/libreadline.a


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{_mingw32_bindir}/readline.dll
%{_mingw32_bindir}/history.dll
%{_mingw32_libdir}/readline.dll.a
%{_mingw32_libdir}/history.dll.a
%{_mingw32_includedir}/readline/


%changelog
* Wed Nov 19 2008 Richard W.M. Jones <rjones@example.com> - 5.2-3
- Fix paths to mandir, infodir.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@example.com> - 5.2-2
- Rebuild against latest termcap.

* Thu Sep 25 2008 Richard W.M. Jones <rjones@example.com> - 5.2-1
- Initial RPM release.
