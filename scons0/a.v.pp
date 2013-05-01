[:$cc=2;
$dd=2;
]:
`ifdef SOMEONE
:foreach my $pp ($a..$b) {
module a(`SOMEONE,`$d`,`HELLO`$cc`,`$dd*2`);
:}
endmodule
`endif
