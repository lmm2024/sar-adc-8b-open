module oa_sar8_core16 (
`ifdef USE_POWER_PINS
    inout VDD,
    inout VSS,
`endif
    output busy,
    input  clk,
    output done,
    input  rst_n,
    input  start,
    input  vcm,
    input  vinn,
    input  vinp,
    output [7:0] result
);
endmodule
