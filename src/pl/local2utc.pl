#!/usr/bin/env perl
use strict;
use DateTime;
use Date::Parse qw(str2time);

my $pattern = qr/\d?\d:\d\d(:\d\d)?(?: ?[aApP][mM])?/;

while (<>) {
    s/$pattern/utc(str2time($&), $1)/eg;
    print;
}

sub utc {
    my($epoch, $sec) = @_;

    my $utc = DateTime->from_epoch(
        epoch => $epoch,
        time_zone => "UTC",
    );

    $utc->strftime( defined $sec ? "%H:%M:%S" : "%H:%M" );
}
