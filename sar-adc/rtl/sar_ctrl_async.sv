// OA-SAR8: asynchronous (self-timed) SAR controller — golden behavioral model.
//
// Operation: `track` high = sampling. On the falling edge of `track` the
// conversion launches. The comparator is strobed by `cmp_fire`; when its
// completion detector reports `cmp_valid`, the decision `cmp` is absorbed,
// the next trial bit is armed, and the comparator is reset (cmp_fire drops
// because valid is high). When valid falls again, cmp_fire re-arms: the loop
// self-oscillates through all N bits with no bit clock.
//
// In silicon the completion detector is (outp XOR outn) of the StrongARM
// latch and this block becomes a small custom/self-timed macro; this RTL is
// the golden reference for simulation and for the sync-vs-async comparison.
module sar_ctrl_async #(
    parameter int N = 8
) (
    input  logic         rst_n,
    input  logic         track,      // high: track/sample; falling edge starts conversion
    input  logic         cmp,        // comparator decision (valid when cmp_valid=1)
    input  logic         cmp_valid,  // comparator completion flag
    output logic         cmp_fire,   // comparator strobe (self-timed ring)
    output logic [N-1:0] dac_code,
    output logic         busy,
    output logic         done,
    output logic [N-1:0] result
);

    logic [N-1:0] mask;

    assign cmp_fire = busy && !cmp_valid;

    always @(negedge rst_n, negedge track, posedge cmp_valid) begin
        if (!rst_n) begin
            busy     <= 1'b0;
            done     <= 1'b0;
            dac_code <= '0;
            mask     <= '0;
            result   <= '0;
        end else if (!track && !busy && !cmp_valid) begin
            // conversion launch: arm MSB trial
            busy     <= 1'b1;
            done     <= 1'b0;
            mask     <= 1 << (N - 1);
            dac_code <= 1 << (N - 1);
        end else if (cmp_valid && busy) begin
            if (mask == 1) begin
                // final bit resolved
                result <= cmp ? dac_code : (dac_code & ~mask);
                busy   <= 1'b0;
                done   <= 1'b1;
            end else begin
                dac_code <= (cmp ? dac_code : (dac_code & ~mask)) | (mask >> 1);
                mask     <= mask >> 1;
            end
        end
    end

endmodule
