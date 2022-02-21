#!/usr/bin/env perl
use strict;

my $WORD_LIST_PATH = "/Users/jerome/projects/wordle/five_letter_words.txt";

sub all_in_letters {
   my($word, $in_str) = @_;
   my %word_dict = map{$_=>1} split '', $word;
   for my $letter (split '', $in_str) {
      return 0 unless $word_dict{$letter};
   }
   return 1;
}

die "Usage: $0 'placed' 'in' 'out'" if @ARGV != 3;
my ($placed, $in, $out) = @ARGV;
open(WORDS, $WORD_LIST_PATH) || die "Can't read-open $WORD_LIST_PATH: $!";
my $re = '(?=' . join('.*', ("[$in]")x(length($in))) . ')';
while( <WORDS> ) {
   chomp;
   next if $placed && ! /^$placed/;
   next if /[$out]/;
   print "$_\n" if ! $in or all_in_letters($_, $in);
}
close WORDS;

