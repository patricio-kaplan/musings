module fifo 
	#(parameter DEPTH=4
	 ,parameter WIDTH=256
	)
	( input wire clk
	, input wire rst
	, input wire wr
	, input wire rd
	, input wire[WIDTH-1:0] wr_data
	, output wire[WIDTH-1:0] rd_data
	, output wire empty
	, output wire full
	);

localparam DLG2 = $clog2(DEPTH);

reg [WIDTH-1:0] mem[0:DEPTH-1];

reg [DLG2:0] wrptr, rdptr, wrptr_nxt, rdptr_nxt;

always @(posedge clk) begin
	if (rst) begin
		wrptr<='d0;
		rdptr<='d0;
	end else begin
		wrptr<=wrptr_nxt;
		rdptr<=rdptr_nxt;
	end
end
always @(posedge clk) begin
	if (wr) mem[wrptr[DLG2-1:0]] <= wr_data;
end

always @(*) begin
	wrptr_nxt = wrptr + {{DLG2{1'b0}}, wr};
	rdptr_nxt = rdptr + {{DLG2{1'b0}}, rd};
	rd_data = mem[rdptr[DLG2-1:0]];
	empty = (wrptr==rdptr);
	full = (wrptr[DLG2-1:0]==rdptr[DLG2-1:0]) & (wrptr[DLG2]!=rdptr[DLG2]);
end

endmodule
