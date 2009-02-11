#!/usr/bin/perl -w
#
# CrossReport - analysis tool.
# Copyright (C) 2009 Red Hat Inc.
# Written by Richard W.M. Jones <rjones@redhat.com>,
# http://fedoraproject.org/wiki/MinGW
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

use strict;
use utf8;

# This removes "Wide character in print" warning.  Perl should do
# the right thing based on the locale, but it doesn't, so ...
binmode STDOUT, ":utf8";

use Getopt::Long;
use Pod::Usage;
use GDBM_File;
use POSIX qw(strftime floor);

=pod

=head1 NAME

CrossReport - Analysis tool to help cross-compilation to Windows.

=head1 SYNOPSIS

 mingw32-crossreport [options] /path/to/linuxbinary

=head1 DESCRIPTION

CrossReport is a tool to help you analyze the APIs used by a compiled
Linux program, in order to work out the effort required to
cross-compile that program for Windows, using the Fedora MinGW
cross-compiler.

The simplest way to use it is to point it at an existing Linux binary,
and then read the generated report.

What it does in more detail: It looks at the libraries and API calls
used by the Linux binary, and compares them to the libraries and API
calls that we currently support under the Fedora MinGW cross-compiler.
It then works out what is missing, and produces a report suggesting
the amount of work that needs to be done to port the program.  For
example, whether whole libraries need to be ported first, and/or how
to substitute individual calls to work on Windows.

=head1 EXAMPLE

Assuming that the excellent vector graphics editor Inkscape
(L<http://www.inkscape.org/>) is installed, you could do:

 mingw32-crossreport /usr/bin/inkscape > inkscape-report.txt
 less inkscape-report.txt

=head1 SHORTCOMINGS

The report is only a general guide.  CrossReport contains a lot of
knowledge about common Linux calls and APIs, but does not know about
every possible library.

=head1 DATABASE

The program relies on a database of MinGW APIs.  The default location
for this database is C</usr/share/crossreport/crossreport.db> or the
same file in the current working directory.  If the database cannot be
found in either location, the program will fail with an error message.

The database is updated regularly and distributed with CrossReport.
To get the best quality report, make sure you are running a recent
version of the program.

=cut

my $help = '';
my $man = '';
my $verbose = '';
my $binary = '';

sub get_options
{
    my $result = GetOptions (
	"help|?" => \$help,
	"man" => \$man,
	"verbose" => \$verbose,
    );
    die "crossreport: use --help for information about command line options\n"
	unless $result;

    pod2usage(1) if $help;
    pod2usage(-exitstatus => 0, -verbose => 2) if $man;

    die "crossreport: no binary specified: use --help for more help\n"
	if @ARGV != 1;

    $binary = $ARGV[0];
}

my %symbols;

sub get_db
{
    foreach ("/usr/local/share/crossreport/crossreport.db",
	     "/usr/share/crossreport/crossreport.db",
	     "crossreport.db") {
	if (-f $_) {
	    tie %symbols, "GDBM_File", $_, &GDBM_READER, 0;
	    return;
	}
    }
    die "Could not find crossreport.db\n"
}

# Get the symbols (API calls) used by the binary.

my %api = ();			# Count how each API is used.
my @unresolved = ();		# List of unresolved symbols.

sub get_symbols
{
    my $cmd = "nm -D $binary | grep ' U ' | awk '{print \$2}' | c++filt";
    open CMD, "$cmd |" or die "$cmd: $!";
    foreach (<CMD>) {
	chomp;
	if (exists $symbols{$_}) {
	    my $rpm_name = $symbols{$_};
	    $api{$rpm_name} = 0 unless exists $api{$rpm_name};
	    $api{$rpm_name}++;
	} else {
	    push @unresolved, $_;
	}
    }
    close CMD;
}

#----------------------------------------------------------------------
# Reporting section.

# This hash contains our area expertise about some unresolved symbols.

my $suggest_portability_library =
    "To get more reliable semantics, we suggest you use a portability\n".
    "library such as Gnulib, glib2, QtCore, etc.\n";
my $warning_about_read_write_on_sockets =
    "If you are using read/write on sockets, then this won't work on\n".
    "Windows.  You should use recv/send instead.\n";
my $ifdef_win32 =
    "Use #ifndef WIN32 ... #else ... #endif around the Linux/Windows API\n".
    "differences to ensure that your code continues to compile on Linux.\n";

my %report = (
    open =>
    "Program uses POSIX open/close/read/write/... APIs.  You should be\n".
    "aware that Win32 provides functions with the same name which do not\n".
    "have POSIX semantics.  Simple file operations will be fine, but you\n".
    "will not be able to, for example, open /dev/* or other special files,\n".
    "and select, locking and other POSIX features will not work the same\n".
    "way.\n".
    "\n".
    "$suggest_portability_library".
    "\n".
    "$warning_about_read_write_on_sockets",
    close => '@open',
    read => '@open',
    write => '@open',

    socket =>
    "Program uses Berkeley sockets API.  Windows has a reasonable facsimile\n".
    "called Winsock.  However it has some annoying API differences, in\n".
    "particular: (1) You have to use WSAGetLastError instead of errno,\n".
    "(2) error numbers have different names, (3) you cannot select on,\n".
    "sockets, (4) a multitude of small API differences, (5) you have to\n".
    "initialize Winsock before using it by calling WSAStartup.\n".
    "\n".
    "$ifdef_win32".
    "\n".
    "$suggest_portability_library".
    "\n".
    "$warning_about_read_write_on_sockets",
    socketpair => '@socket',
    accept => '@socket',
    bind => '@socket',
    connect => '@socket',
    listen => '@socket',
    getsockopt => '@socket',
    setsockopt => '@socket',
    shutdown => '@socket',

    ioctl =>
    "Program uses fcntl or ioctl system calls.  Only a tiny fraction of\n".
    "the functionality of these system calls is available in Windows,\n".
    "often with differences in semantics.\n".
    "\n".
    "$suggest_portability_library",
    fcntl => '@ioctl',

    select =>
    "The select/poll/etc system calls are not available on Windows.  You\n".
    "have to use WSAWaitForMultipleEvents instead.\n".
    "\n".
    "$ifdef_win32".
    "\n".
    "$suggest_portability_library",
    poll => '@select',
    epoll_create => '@select',
    epoll_ctl => '@select',
    epoll_wait => '@select',

    fork =>
    "You cannot use fork to create new processes under Windows.  You have\n".
    "to replace calls to fork/exec with CreateProcess or CreateThread.\n".
    "\n".
    "If your program forks in order to run in parallel or to create\n".
    "multiple identical workers, then you may have to restructure the\n".
    "program.\n".
    "\n".
    "If your program needs to share resources such as file descriptors\n".
    "across the fork, then some limited options are available through\n".
    "CreateProcess, but nothing like as rich as what is available in\n".
    "Unix.\n".
    "\n".
    "$ifdef_win32".
    "\n".
    "For server programs, we suggest using a portability library tuned\n".
    "for the needs of servers, such as Apache Portable Runtime.\n",
    execl => '@fork',
    execlp => '@fork',
    execle => '@fork',
    execv => '@fork',
    execvp => '@fork',
    execve => '@fork',

    usleep =>
    "usleep/nanosleep system calls do not exist on Windows.  You should\n".
    "replace this with one of the Win32 equivalents such as Sleep.\n".
    "\n".
    "$ifdef_win32".
    "\n".
    "$suggest_portability_library",
    nanosleep => '@usleep',

    dup =>
    "dup/dup2 may not work as expected in Win32.\n".
    "\n".
    "$suggest_portability_library",
    dup2 => '@dup2',

    getopt_long =>
    "GNU getopt_long is not available in Windows.\n".
    "\n".
    "$suggest_portability_library",

    __stack_chk_fail =>
    "The -fstack-protector option may not work with the Fedora MinGW\n".
    "cross-compiler at this time.\n",

    fopen =>
    "fopen/fclose/... work for simple file operations on Windows.  If you\n".
    "are using binary files, you must add the 'b' character to the fopen\n".
    "call, otherwise Windows will try to do line-end translation.  The\n".
    "'b' works on Linux (it is silently ignored).\n",
    fclose => '@fopen',
    fread => '@fopen',
    fwrite => '@fopen',
    fseek => '@fopen',
    fgetpos => '@fopen',
    feof => '@fopen',
    fflush => '@fopen',
    fseek => '@fopen',

    getenv =>
    "clearenv/getenv/putenv/setenv/unsetenv and direct access to environ\n".
    "should be used with care under Windows.  Commonly available environment\n".
    "variables may not exist in Windows, and Windows does not have any\n".
    "simple mechanism for setting environment variables.\n".
    "\n".
    "$suggest_portability_library",
    clearenv => '@getenv',
    putenv => '@getenv',
    setenv => '@getenv',
    unsetenv => '@getenv',

    tmpfile =>
    "tmpfile is available on Windows, but the function is deprecated by\n".
    "Microsoft in favour of a secure but proprietary replacement\n".
    "(tmpfile_s).  You might consider using the replacement function on\n".
    "Windows.\n".
    "\n".
    "$ifdef_win32",

    rename =>
    "rename is available on Windows, but it may not have the atomic\n".
    "properties found on some Unix variants.  Do not rely on this as a\n".
    "replacement for file locking.\n",

    scanf =>
    "scanf/sscanf is available on Windows, but behaves differently: it does\n".
    "not automatically skip whitespace before %-specifiers.  If your code\n".
    "relies on this, then you may need to modify it.\n".
    "\n".
    "See: http://msdn.microsoft.com/en-us/library/kwwtf9ch(VS.71).aspx\n",
    sscanf => '@scanf',

    signal =>
    "Signal handling under Windows is very different/limited compared to\n".
    "Unix.  It is likely that your code will need careful inspection if\n".
    "it does anything non-trivial with signals.\n".
    "\n".
    "See: http://msdn.microsoft.com/en-us/library/xdkz3x12(VS.71).aspx\n",
    sigaction => '@signal',
    kill => '@signal',

    popen =>
    "popen/pclose exist in a some form under Windows (as _popen/\n".
    "_pclose), but have many limitations and you should generally avoid\n".
    "using them.\n".
    "\n".
    "See: http://msdn.microsoft.com/en-us/library/96ayss4b(VS.80).aspx\n".
    "\n".
    "$suggest_portability_library",
    pclose => '@popen',

    mkdir =>
    "mkdir exists in several different forms on various platforms.\n".
    "\n".
    "$suggest_portability_library",

    strtoll =>
    "stroll/strtold/strtoul/strtoull do not exist on Windows.\n".
    "\n".
    "$suggest_portability_library",
    strtold => '@strtoll',
    strtoul => '@strtoll',
    strtoull => '@strtoull',

    system =>
    "You should be careful using the 'system' call on Windows.  It exists\n".
    "but the commands that it runs are quite different.  Available commands,\n".
    "paths, shells, redirection, directory separators, etc. are all likely\n".
    "to be incompatible with Linux.\n",

    rand =>
    "The standard random functions are useless in Windows since they return\n".
    "only a very limited range of numbers and do not have good randomness.\n".
    "\n".
    "$suggest_portability_library",
    srand => '@rand',

    regcomp =>
    "Win32 does not have POSIX regular expression parsing (regcomp/\n".
    "regexec/etc.)  Use an external regular expression library instead.\n",
    regexec => '@regcomp',
    regfree => '@regcomp',

    wait =>
    "Win32 does not support wait/waitpid system calls.  You will have to\n".
    "rewrite code that depends on waiting & PIDs using Win32 specific APIs.\n".
    "\n".
    "$ifdef_win32".
    "\n".
    "$suggest_portability_library",
    waitpid => '@wait',
    waitid => '@wait',
    wait4 => '@wait',






);

# Additional reports, so we can match by regular expression.
# Returns a string, or undef if no match.

sub report_extra
{
    local $_ = shift;		# Symbol.

    if (m/^X[A-Z][A-Za-z0-9]+$/) {
	return
	"X11 is not available on Windows, and in general your program\n".
	"will not be talking to an X server.  Replace any X11 calls with\n".
	"calls to a higher-level portable library like Gtk or Qt.\n";
    }

    if (m/^dbus_$/) {
	return
	"The DBus API has proven problematic to port to Windows in the\n".
	"past.  For the latest information about this, contact the\n".
	"Fedora MinGW mailing list.\n";
    }

    return undef;
}

# List of symbols for which there is no known problem.

my %no_report = (
    __assert_fail => 1,
    __dynamic_cast => 1,
    __errno_location => 1,
    __libc_start_main => 1,
    _IO_getc => 1,
    _IO_putc => 1,
    _Unwind_Resume => 1,
    _exit => 1,
    abort => 1,
    acos => 1,    # XXX any incompatibility in math library calls?
    asin => 1,
    atan => 1,
    atan2 => 1,
    cabs => 1,
    calloc => 1,
    ceil => 1,
    ceilf => 1,
    cos => 1,
    exit => 1,
    fgetc => 1,
    fgets => 1,
    floor => 1,
    floorf => 1,
    fmod => 1,
    fputc => 1,
    fputs => 1,
    free => 1,
    malloc => 1,
    memchr => 1,
    memcpy => 1,
    memmove => 1,
    memset => 1,
    perror => 1,
    recv => 1,
    send => 1,
    setlocale => 1,
    sqrt => 1,
    sin => 1,
    strcasecmp => 1,
    strchr => 1,
    strcmp => 1,
    strcpy => 1,
    strdup => 1,
    strftime => 1,
    strlen => 1,
    strncmp => 1,
    strncpy => 1,
    strrchr => 1,
    strspn => 1,
    strstr => 1,
    strtod => 1,
    strtol => 1,
    tan => 1,
);

sub no_report_extra
{
    local $_ = shift;

    return 1 if m/^__cxa_/;
    return 1 if m/^operator new\(/;
    return 1 if m/^operator new\[/;
    return 1 if m/^__\w+_chk$/;
    return 1 if m/^gtk_x11_/;
    return 0
}

sub report_start
{
    my $time = time ();
    my $date = strftime "%a %b %e %H:%M:%S %Y", localtime ($time);
    my $sym_time = $symbols{__crossreport_time};
    my $sym_date = strftime "%a %b %e %H:%M:%S %Y", localtime ($sym_time);
    my $days = floor (($time - $sym_time) / 86400);

    print <<EOT;
----------------------------------------------------------------------
Cross-compilation report for: $binary
----------------------------------------------------------------------

1. INTRODUCTION

Report prepared on $date.
Symbol database last updated on $sym_date ($days days ago).

EOT
}

# Report resolved libraries.

sub report_resolved
{
    print <<EOT;
2. SUPPORTED APIs USED BY THE PROGRAM

This table shows the supported APIs that this program uses,
including the number of different calls made to each API.
In most cases, you just need to arrange it so that your program
'BuildRequires' these RPMs and links to the libraries within them.

      #calls  RPM name
EOT

    foreach (sort (keys %api)) {
	printf "  %10d  %s\n", $api{$_}, $_;
    }

    print "\n";
}

# Report unresolved symbols.

sub report_unresolved
{
    @unresolved = sort @unresolved;

    if (0 == @unresolved) {
	print <<EOT;
3. UNSUPPORTED APIs USED BY THE PROGRAM

No unresolved symbols were found.  Programs which have no
unresolved symbols at all are the easiest to port because
portability libraries (eg. glib, Qt) have already done all
the hard work for you.
EOT
    } else {
	my $nr_unresolved = @unresolved;
	print <<EOT;
3. UNSUPPORTED APIs USED BY THE PROGRAM

$nr_unresolved unresolved symbols were found.  The full list of symbols
is listed as an appendix at the end of this report.  In this
section we try to identify known portability problems from
this list of symbols.

EOT

        foreach (@unresolved) {
	    if (!exists $no_report{$_} && !no_report_extra($_)) {
		if (exists $report{$_}) {
		    my $r = $report{$_};
		    $r = $report{$1} while $r =~ /@(.*)/;
		    print "--- Program uses: $_\n\n$r\n";
		} else {
		    my $r = report_extra ($_);
		    print "--- Program uses: $_\n\n$r\n" if defined $r;
		}
	    }
        }


        print <<EOT;
APPENDIX - FULL LIST OF UNRESOLVED SYMBOLS

* = Symbol we were not able to give advice about.  If you know
    more about this symbol, consider providing a patch for the
    CrossReport program.

\x{2714} = Win32 should supply this symbol, or it can be ignored because
    it is a side-effect of the Unix toolchain.

\x{2191} = Read the report above for advice about using this symbol.

EOT

	foreach (@unresolved) {
	    my $star = " ";
	    if (exists $no_report{$_} || no_report_extra($_)) {
		$star = "\x{2714}";
	    } else {
		$star = "*";
		$star = "\x{2191}" if exists $report{$_};
		my $r = report_extra ($_);
		$star = "\x{2191}" if defined $r;
	    }
	    print "\t$star $_\n"
        }
    }

    print "\n";
}

sub report_links
{
    print <<EOT;
USEFUL LINKS

http://www.gnu.org/software/gnulib/  Gnulib (portability library)
http://library.gnome.org/devel/glib/ Glib reference manual
http://www.gtk.org/                  Gtk+
http://www.qtsoftware.com/products   Qt
http://apr.apache.org/               Apache Portable Runtime
http://msdn.microsoft.com/           Microsoft Developer Network
http://fedoraproject.org/wiki/MinGW  Fedora MinGW project
EOT
}

# Main program.

sub main
{
    get_options ();
    get_db ();
    get_symbols ();
    report_start ();
    report_resolved ();
    report_unresolved ();
    report_links ();
}

main ();

=pod

=head1 COPYRIGHT

Copyright (C) 2009 Red Hat Inc.
Written by Richard W.M. Jones <rjones@redhat.com>.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

=cut
