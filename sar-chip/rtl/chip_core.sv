// SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
// OA-SAR8 chip core: one hard macro (oa_sar8_core16 = 8-bit differential SAR ADC,
// 10 MS/s, 1.5 V; closed-loop fixed: comparator clock from the SAR logic, SR-latched
// comparator outputs, corrected CDAC polarity) wired to the padframe.
`default_nettype none

module chip_core #(
    parameter int unsigned NUM_INPUT_PADS,
    parameter int unsigned NUM_OUTPUT_PADS,
    parameter int unsigned NUM_BIDIR_PADS,
    parameter int unsigned NUM_ANALOG_PADS
)(
    `ifdef USE_POWER_PINS
    inout  wire VDD,
    inout  wire VSS,
    `endif
    input  logic clk,
    input  logic rst_n,
    input  logic [NUM_INPUT_PADS-1 :0] input_in,
    output logic [NUM_OUTPUT_PADS-1:0] output_out,
    input  logic [NUM_BIDIR_PADS-1 :0] bidir_in,
    output logic [NUM_BIDIR_PADS-1 :0] bidir_out,
    output logic [NUM_BIDIR_PADS-1 :0] bidir_oe,
    inout  wire  [NUM_ANALOG_PADS-1:0] analog_padres,
    inout  wire  [NUM_ANALOG_PADS-1:0] analog_padbare
);
    // analog inputs: vinp / vinn / vcm through the pad secondary ESD (padres)
    wire vinp = analog_padres[0];
    wire vinn = analog_padres[1];
    wire vcm  = analog_padres[2];

    wire [7:0] result;
    wire done, busy;

    oa_sar8_core16 sar_adc (
        `ifdef USE_POWER_PINS
        .VDD    (VDD),
        .VSS    (VSS),
        `endif
        .clk    (clk),
        .rst_n  (rst_n),
        .start  (input_in[0]),
        .vinp   (vinp),
        .vinn   (vinn),
        .vcm    (vcm),
        .result (result),
        .done   (done),
        .busy   (busy)
    );

    assign output_out[7:0] = result;
    assign output_out[8]   = done;
    assign output_out[9]   = busy;
    assign output_out[NUM_OUTPUT_PADS-1:10] = '0;  // spare outputs driven low

    // spare bidir: input mode, driven low
    assign bidir_out = '0;
    assign bidir_oe  = '0;
endmodule

`default_nettype wire
