:$pp=0;
[:$cc=2;
$dd=2;
]:
`ifdef SOMEONE
:foreach my $pp (0..9) {
module a(`SOMEONE,`$pp`,`HELLO`$cc`,`$dd*2`);
:}
endmodule
`endif
