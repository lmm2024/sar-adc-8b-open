// Gate-level activity TB for sar_ctrl (post-PnR netlist): back-to-back conversions
// at 10 MS/s (100 MHz clock, 10 cycles per conversion incl. sample), sine input,
// behavioral ideal CDAC/comparator. Dumps VCD for OpenSTA read_vcd power.
`timescale 1ns / 1ps
module tb_gl_power;
    localparam int  N    = 8;
    localparam real VREF = 1.5;
    localparam real LSB  = VREF / (2.0 ** N);
    logic clk = 0, rst_n = 0, start = 0, cmp;
    wire [N-1:0] dac_code, dac_code_n, result;
    wire sample, busy, done;
    real vin, vin_s, vdac;

    sar_ctrl dut (
        .clk(clk), .rst_n(rst_n), .start(start), .cmp(cmp),
        .dac_code(dac_code), .dac_code_n(dac_code_n), .sample(sample),
        .busy(busy), .done(done), .result(result));

    always #5 clk = ~clk;                       // 100 MHz
    always @(posedge clk) if (sample) vin_s <= vin;
    always @* vdac = $itor(dac_code) * LSB;
    assign cmp = (vin_s > vdac);

    real t;
    initial begin
        $dumpfile("/foss/designs/sar-adc/power/sar_gl.vcd");
        $dumpvars(0, tb_gl_power.dut);
        vin = 0.75;
        repeat (3) @(negedge clk);
        rst_n = 1;
        // 200 conversions back-to-back: start pulse every 10 cycles, vin = 0.75 + 0.7 sin
        for (int i = 0; i < 200; i++) begin
            vin = 0.75 + 0.7 * $sin(2.0 * 3.14159265 * i / 37.0);
            @(negedge clk) start = 1;
            @(negedge clk) start = 0;
            repeat (8) @(negedge clk);
        end
        $finish;
    end
endmodule
