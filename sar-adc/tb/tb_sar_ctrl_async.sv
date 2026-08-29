// Self-checking TB for the asynchronous SAR controller.
// Comparator modeled with RANDOM decision delay (0.5–3 ns) + reset delay,
// exercising the self-timed handshake. Also reports conversion time.
`timescale 1ns / 1ps
module tb_sar_ctrl_async;
    localparam int  N    = 8;
    localparam real VREF = 1.5;
    localparam real LSB  = VREF / (2.0 ** N);

    logic rst_n = 1, track = 1, cmp = 0, cmp_valid = 0;
    logic cmp_fire, busy, done;
    logic [N-1:0] dac_code, result;
    real vin, vin_s, vdac;

    sar_ctrl_async #(.N(N)) dut (.*);

    always @* vdac = $itor(dac_code) * LSB;

    // behavioral StrongARM: fires on cmp_fire, resolves after a random delay
    real d;
    always @(posedge cmp_fire) begin
        d = $urandom_range(50, 300) / 100.0;  // 0.5 - 3.0 ns
        #(d);
        if (cmp_fire) begin
            cmp       <= (vin_s > vdac);
            cmp_valid <= 1'b1;
        end
    end
    always @(negedge cmp_fire) begin
        #(0.3);
        cmp_valid <= 1'b0;
    end

    int n_pass = 0, n_fail = 0;
    real t0, tconv_sum = 0.0;
    int  nconv = 0;

    task automatic convert(input real v, output int code);
        vin = v;
        wait (busy === 1'b0);      // previous conversion fully finished
        track = 1;
        #(20);
        vin_s = vin;               // value held at end of track phase
        t0 = $realtime;
        track = 0;                 // falling edge: conversion starts
        @(posedge done);           // edge, not level: immune to stale done
        tconv_sum += ($realtime - t0);
        nconv++;
        code = result;
        #(2);
    endtask

    initial begin
        #(50_000_000);             // 50 ms watchdog
        $display("WATCHDOG TIMEOUT: busy=%b done=%b fire=%b valid=%b", busy, done, cmp_fire, cmp_valid);
        $finish;
    end

    function automatic int expected(input real v);
        int e;
        if (v <= 0.0) return 0;
        e = $rtoi($floor(v / LSB));
        return (e > 2 ** N - 1) ? 2 ** N - 1 : e;
    endfunction

    initial begin
        #(2) rst_n = 0;            // real negedge so the async reset branch fires
        #(8) rst_n = 1;

        for (int k = 0; k < 2 ** N; k++) begin
            int c;
            convert((k + 0.5) * LSB, c);
            if (c == k) n_pass++;
            else begin
                n_fail++;
                $display("FAIL mid-code k=%0d got %0d", k, c);
            end
        end
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
        begin
            int c;
            convert(-0.05, c);
            if (c == 0) n_pass++; else begin n_fail++; $display("FAIL under-range"); end
            convert(VREF + 0.05, c);
            if (c == 2 ** N - 1) n_pass++; else begin n_fail++; $display("FAIL over-range"); end
        end

        $display("RESULT: pass=%0d fail=%0d", n_pass, n_fail);
        $display("avg conversion time = %.2f ns (8 self-timed bit cycles)", tconv_sum / nconv);
        if (n_fail == 0) $display("ALL TESTS PASSED");
        $finish;
    end
endmodule
