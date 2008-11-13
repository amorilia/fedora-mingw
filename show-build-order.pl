#!/usr/bin/perl -w
#
# Show the order to build Fedora MinGW spec files.
# By Richard Jones <rjones@redhat.com>

use strict;

my $debug = 0;
chomp (my $pwd = `pwd`);

sub main {
    my %br;
    my $specfile;
    my $packagename;

    my @specfiles = <*/*.spec>;

    # Get BRs for each specfile.
    foreach $specfile (@specfiles) {
	$packagename = $specfile;
	$packagename =~ s{^.*/}{};
	$packagename =~ s{\.spec$}{};

	$br{$packagename} = [];

	open SPEC,$specfile or die "$specfile: $!";
	while (<SPEC>) {
	    if (m/^BuildRequires:(.*)/) {
		my $brs = $1;
		my @brs = eval 'split /,/, $brs';
		@brs = map { trim ($_) } @brs;
		@brs = map { remove_trailers ($_) } @brs;
		unshift @{$br{$packagename}}, @brs;
	    }
	}

	if ($debug) {
	    print "BRs for $packagename = [";
	    print (join "],[", @{$br{$packagename}});
	    print "]\n";
	}
    }

    foreach $packagename (keys %br) {
	my @brs = @{$br{$packagename}};
	@brs = uniq (sort @brs);
	$br{$packagename} = \@brs;

	if ($debug) {
	    print "uniq BRs for $packagename = [";
	    print (join "],[", @{$br{$packagename}});
	    print "]\n";
	}
    }

    # Some packages we want to ignore for now.
    delete $br{"mingw32-cyrus-sasl"};
    delete $br{"mingw32-wix"};
    delete $br{"mingw32-example"};
    delete $br{"mingw32-gdb"};
    delete $br{"mingw32-python"};
    delete $br{"mingw32-ocaml"};
    delete $br{"mingw32-curl"};
    delete $br{"mingw32-pidgin"};
    delete $br{"mingw32-nspr"};
    delete $br{"mingw32-nss"};

    # There is a dependency loop (gcc -> runtime/w32api -> gcc)
    # which has to be manually resolved below.  Break that loop.
    my @gcc_brs = @{$br{"mingw32-gcc"}};
    @gcc_brs = grep { $_ ne "mingw32-runtime" && $_ ne "mingw32-w32api" } @gcc_brs;
    $br{"mingw32-gcc"} = \@gcc_brs;

    # Use tsort to generate a topological ordering.
    open TSORT,">/tmp/tsort.tmp" or die "/tmp/tsort.tmp: $!";
    foreach $packagename (keys %br) {
	my $br;
	foreach $br (@{$br{$packagename}}) {
	    print "writing $br $packagename\n" if $debug;
	    print TSORT $br, " ", $packagename, "\n";
	}
    }
    close TSORT;

    system ("tsort < /tmp/tsort.tmp > /tmp/tsort2.tmp") == 0
	or die "system: tsort: $?";

    # Read in list of packages.
    open PACKAGES,"/tmp/tsort2.tmp" or die "/tmp/tsort2.tmp: $!";
    unless ($debug) {
	unlink "/tmp/tsort.tmp";
	unlink "/tmp/tsort2.tmp";
    }

    my %installed;

    while (<PACKAGES>) {
	chomp;
	if (/^mingw32-(.*)/ && exists $br{$_}) {
	    $packagename = $_;
	    my $dirname = $1;

	    print "considering $packagename\n" if $debug;

	    my @brs = @{$br{$packagename}};

	    # Are all BR RPMs installed?
	    my $br;
	    foreach $br (@brs) {
		if (! rpm_installed ($br) && !exists $installed{$br}) {
		    print "# as root: rpm -Uvh $br*.rpm\n";
		    $installed{$br} = 1;
		}
	    }

	    # Special case for mingw32-gcc deps.
	    if ($packagename eq "mingw32-gcc" &&
		(!rpm_installed ("mingw32-runtime") ||
		 !rpm_installed ("mingw32-w32api"))) {
		print "rpmbuild -ba --define \"_sourcedir $pwd/runtime-bootstrap\" runtime-bootstrap/mingw32-runtime-bootstrap.spec\n";
	        print "# as root: rpm -Uvh mingw32-runtime-bootstrap*.rpm\n";
		$installed{"mingw32-runtime-bootstrap"} = 1;

		print "rpmbuild -ba --define \"_sourcedir $pwd/w32api-bootstrap\" w32api-bootstrap/mingw32-w32api-bootstrap.spec\n";
	        print "# as root: rpm -Uvh mingw32-w32api-bootstrap*.rpm\n";
		$installed{"mingw32-w32api-bootstrap"} = 1;
	    }

	    # Spec file.
	    my $specfile = "$dirname/$packagename.spec";
	    die "$specfile: file missing" unless -f $specfile;

	    my $rpmbuild =
		"rpmbuild -ba --define \"_sourcedir $pwd/$dirname\"";
	    print "$rpmbuild $specfile\n";
	}
    }
}

sub rpm_installed {
    local $_ = shift;
    return (system ("rpm -q $_ > /dev/null") == 0);
}

sub trim {
    local $_ = shift;
    s/^\s+//;
    s/\s+$//;
    return $_;
}

sub uniq {
    my %hash;
    local $_;

    $hash{$_} = 1 foreach (@_);
    return sort keys %hash;
}

# foo >= 3.1 --> foo
# foo-devel --> foo
# and a few other exceptions
sub remove_trailers {
    local $_ = shift;
    s/\s*[<>=].*$//;

    # -devel & -doc come from the base package.
    s/-devel$//;
    s/-doc$//;

    # mingw32-gcc-c++ etc.
    s/^mingw32-gcc-.*/mingw32-gcc/;

    return $_;
}

&main()
