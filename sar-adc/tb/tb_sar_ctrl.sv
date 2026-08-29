// Self-checking TB for sar_ctrl v3: behavioral track/hold + ideal CDAC + a
// StrongARM-like comparator model (precharged high while clk_cmp=0, one output
// drops ~1 ns after clk_cmp rises). Checks single conversions, random inputs,
// rails, and back-to-back operation at 11 clocks per conversion (3 track clocks).
`timescale 1ns / 1ps
module tb_sar_ctrl;
    localparam int  N    = 8;
    localparam real VREF = 1.5;
    localparam real LSB  = VREF / (2.0 ** N);

    logic clk = 0, rst_n = 0, start = 0;
    logic cmp, cmp_n, clk_cmp, hold;
    logic [N-1:0] dac_code, dac_code_n, result;
    logic sample, busy, done;
    real vin, vin_s, vdac;

    sar_ctrl #(.N(N)) dut (.*);

    always #5 clk = ~clk;

    // behavioral analog: sample-and-hold, ideal DAC, StrongARM-like comparator
    always @(negedge sample) vin_s = vin;          // aperture = end of the track phase
    always @* vdac = $itor(dac_code) * LSB;
    // precharge (both high) while clk_cmp = 0; decision 1 ns after clk_cmp rises
    always @* begin
        if (!clk_cmp) begin cmp = 1'b1; cmp_n = 1'b1; end
    end
    always @(posedge clk_cmp) begin
        #1;
        if (clk_cmp) begin
            cmp   = (vin_s > vdac);
            cmp_n = ~(vin_s > vdac);
        end
    end

    int n_pass = 0, n_fail = 0;

    // timing monitors (real sampling instants only, i.e. when CONV follows): track window
    // >= 24 ns, and the footers (hold) close >= 4 ns after the sampling switches open.
    real t_s_rise, t_s_fall;
    always @(posedge sample) t_s_rise = $realtime;
    always @(negedge sample) t_s_fall = $realtime;
    always @(posedge hold) begin
        #0.1;
        if (dut.state == dut.CONV) begin
            if (t_s_fall - t_s_rise < 24.0) begin n_fail++; $display("FAIL track window %.1f ns", t_s_fall - t_s_rise); end
            if ($realtime - 0.1 - t_s_fall < 4.0) begin n_fail++; $display("FAIL hold rose only %.2f ns after sample fell", $realtime - 0.1 - t_s_fall); end
        end
    end

    task automatic convert(input real v, output int code);
        vin = v;
        @(negedge clk) start = 1;
        @(negedge clk) start = 0;
        wait (done === 1'b1);
        @(negedge clk);
        code = result;
    endtask

    function automatic int expected(input real v);
        int e;
        if (v <= 0.0) return 0;
        e = $rtoi($floor(v / LSB));
        return (e > 2 ** N - 1) ? 2 ** N - 1 : e;
    endfunction

    // back-to-back: start every 10 clocks, results checked as 'done' pulses arrive
    int bb_exp[$];
    int bb_seen = 0;
    always @(posedge clk) if (done && bb_exp.size() > 0) begin
        int e;
        e = bb_exp.pop_front();
        bb_seen++;
        if (result == e) n_pass++;
        else begin n_fail++; $display("FAIL back-to-back #%0d got %0d exp %0d", bb_seen, result, e); end
    end

    initial begin
        repeat (3) @(negedge clk);
        rst_n = 1;

        // every code at its mid-level
        for (int k = 0; k < 2 ** N; k++) begin
            int c;
            convert((k + 0.5) * LSB, c);
            if (c == k) n_pass++;
            else begin
                n_fail++;
                $display("FAIL mid-code k=%0d got %0d", k, c);
            end
        end

        // random voltages
        for (int i = 0; i < 300; i++) begin
            real v;
            int c, e;
            v = $urandom_range(0, 1000000) / 1.0e6 * VREF;
            convert(v, c);
            e = expected(v);
            if (c == e) n_pass++;
            else begin
                n_fail++;
                $display("FAIL v=%.6f got %0d exp %0d", v, c, e);
            end
        end

        // out-of-range rails
        begin
            int c;
            convert(-0.05, c);
            if (c == 0) n_pass++; else begin n_fail++; $display("FAIL under-range got %0d", c); end
            convert(VREF + 0.05, c);
            if (c == 2 ** N - 1) n_pass++; else begin n_fail++; $display("FAIL over-range got %0d", c); end
        end

        // back-to-back: 40 conversions, start pulse every 11 clocks (10 MS/s at 110 MHz)
        begin
            real v;
            repeat (2) @(negedge clk);              // let the previous 'done' pulse pass
            for (int i = 0; i < 40; i++) begin
                v = 0.7513 + 0.7 * $sin(2.0 * 3.14159265 * i / 7.0);   // off the exact code thresholds
                vin = v;
                bb_exp.push_back(expected(v));
                @(negedge clk) start = 1;
                @(negedge clk) start = 0;
                repeat (9) @(negedge clk);
            end
            repeat (14) @(negedge clk);
            if (bb_seen != 40) begin n_fail++; $display("FAIL back-to-back: only %0d done pulses in 40 slots", bb_seen); end
            else $display("back-to-back: 40 conversions in 440 clocks OK");
        end

        $display("RESULT: pass=%0d fail=%0d", n_pass, n_fail);
        if (n_fail == 0) $display("ALL TESTS PASSED");
        $finish;
    end
endmodule
