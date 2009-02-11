#!/usr/bin/perl -w
#
# Update CrossReport database.
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

use GDBM_File;

# Map of symbol name -> RPM owner.
my %symbols;
my $symdbm =
    tie %symbols, "GDBM_File", "crossreport.db", &GDBM_NEWDB, 0666;
main ();
$symbols{__crossreport_time} = time ();
$symdbm->sync ();

sub add_symbol {
    my $symbol = shift;
    my $rpm_name = shift;

    if (exists $symbols{$symbol} &&
	$symbols{$symbol} ne $rpm_name) {
	# Suppress this warning - it is quite common and probably
	# doesn't matter.
        #warn "duplicate symbol: $symbol: $rpm_name and $symbols{$symbol}\n"
    }

    $symbols{$symbol} = $rpm_name;
}

sub main {
    print <<EOT;
Just a note: You should have ALL mingw32-* libraries installed
when you run this, otherwise you will get an incomplete database.
I do not have a way to test this, so I print this note.

EOT

    my @implibs = </usr/i686-pc-mingw32/sys-root/mingw/lib/*.dll.a>;

    print "Analyzing ", 0+@implibs, " libraries ...\n";

    foreach my $implib (@implibs) {
	# What MinGW library provides this file?
	my $cmd = "rpm -qf $implib";
	open CMD, "$cmd |" or die "$cmd: $!";
	my $r = <CMD>;
	close CMD;
	my $rpm_name;
	if ($r =~ /^(mingw32-[-+\w]+)-\d/) {
	    $rpm_name = $1;
	} else {
	    die "$implib: Cannot find RPM owning this file.\n"
	}

	$cmd = "i686-pc-mingw32-nm $implib | grep ' [A-HJ-TV-Z] ' | i686-pc-mingw32-c++filt -_";
	open CMD, "$cmd |" or die "$cmd: $!";
	foreach (<CMD>) {
	    chomp;
	    if (m/^[[:xdigit:]]+ T _(\w+)(@\d+)?$/) {
		add_symbol ($1, $rpm_name);
	    } elsif (m/^[[:xdigit:]]+ T (.*)(@\d+)?$/) {
		add_symbol ($1, $rpm_name);
	    } else {
		die "$_: ?\n";
	    }
	}
    }

    print "Found ", 0+(keys %symbols), " symbols.\n";
}
