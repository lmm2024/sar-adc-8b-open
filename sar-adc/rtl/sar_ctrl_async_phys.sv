// OA-SAR8 physically implementable self-timed SAR controller.
//
// Unlike sar_ctrl_async.sv (the event-driven golden model), this module has:
//   * no # delays;
//   * no register written from several unrelated event blocks;
//   * explicit SG13G2 delay cells for hold and CDAC-settling guards;
//   * one local event clock made from mutually-exclusive launch and comparator
//     completion pulses.
//
// It is intentionally an asynchronous macro.  Conventional single-clock STA
// is not its sign-off method: the request/acknowledge loop must be checked with
// extracted gate/transistor timing after LibreLane placement and routing.
`timescale 1ns / 1ps
module sar_ctrl_async_phys #(
    parameter int N = 8
) (
    input  logic         rst_n,
    input  logic         track,
    input  logic         cmp_p,
    input  logic         cmp_n,

    output logic         cmp_fire,
    output logic         cmp_valid,
    output logic         cmp_fault,
    output logic [N-1:0] dac_code,
    output logic [N-1:0] dac_code_n,
    output logic [N-1:0] bit_active,
    output logic         sample,
    output logic         hold_req,
    output logic         busy,
    output logic         done,
    output logic [N-1:0] result
);
    localparam logic [N-1:0] MSB_MASK = {1'b1, {(N-1){1'b0}}};

    logic track_n;
    logic hold_elapsed;
    logic hold_elapsed_tail;
    logic launch_pulse;
    logic decision_event;
    logic sar_event_raw;
    logic event_pending;
    logic event_pending_reset;
    logic sar_event;

    logic guard_request;
    logic guard_request_delayed;
    logic guard_set;
    logic guard_reset;
    logic settle_ready;

    logic cmp_decision;
    logic cmp_decision_hold;
    logic decision_hold_set;
    logic decision_hold_reset;
    logic [N-1:0] code_reg;
    logic [N-1:0] active_reg;
    logic [N-1:0] resolved_code;

    assign track_n     = ~track;
    assign cmp_valid   = ~(cmp_p & cmp_n);
    assign cmp_fault   = ~cmp_p & ~cmp_n;
    assign cmp_decision = cmp_p & ~cmp_n;

    // Capture the positive comparator rail as an asynchronous event.  A
    // transparent D latch closed from cmp_valid raced the falling comparator
    // rail after full-RC extraction: its gate could close before the inverted
    // decision data arrived, systematically losing high-order one decisions.
    // This physical cross-coupled-NOR latch is reset before every evaluation
    // and set immediately by a positive StrongARM result.  A negative result
    // leaves it reset.  Thus the short valid pulse is retained until the
    // delayed event register clock consumes it, without a behavioural delay.
    assign decision_hold_set = decision_event & cmp_decision;
    assign decision_hold_reset = ~rst_n | ~busy | guard_set;
    (* keep = "true", dont_touch = "true" *)
    sar_async_sr_latch_sg13g2 u_decision_hold (
        .set(decision_hold_set),
        .reset(decision_hold_reset),
        .q(cmp_decision_hold)
    );

    // A delayed copy of ~track implements the break-before-make interval.
    // A second, shorter delayed copy turns its rising edge into a bounded
    // launch pulse.  The comparator must be in its 11 precharge state.
    sar_delay_hold_sg13g2 u_hold_delay (
        .A(track_n),
        .X(hold_elapsed)
    );
    sar_delay_pulsewidth_sg13g2 u_launch_width (
        .A(hold_elapsed),
        .X(hold_elapsed_tail)
    );
    assign launch_pulse = hold_elapsed & ~hold_elapsed_tail
                          & track_n & ~cmp_valid;

    // Comparator completion is the local bit event.  A fault never advances
    // the token; it leaves cmp_fire low for safe diagnosis.
    assign decision_event = busy & cmp_valid & ~cmp_fault;
    assign sar_event_raw  = launch_pulse | decision_event;
    // Capture even a short StrongARM VALID pulse as a level before passing it
    // through the physical setup-time delay.  The delayed output both clocks
    // the register bank and resets the pending latch, so the event pulse at
    // the DFFs is never filtered merely because comparator VALID is narrow.
    // Four-phase return-to-zero acknowledgement.  Do not clear pending merely
    // because the delayed event has risen: comparator VALID may still be high
    // at that instant and would immediately set the latch a second time,
    // consuming one physical decision more than once.  Clear only after both
    // the delayed acknowledgement is present and the raw request has fallen.
    assign event_pending_reset = ~rst_n | (sar_event & ~sar_event_raw);
    sar_async_sr_latch_sg13g2 u_event_pending (
        .set(sar_event_raw),
        .reset(event_pending_reset),
        .q(event_pending)
    );
    sar_delay_event_clock_sg13g2 u_event_clock_delay (
        .A(event_pending),
        .X(sar_event)
    );

    // Start the settling guard from ``sar_event``, the same physical edge that
    // clocks code_reg, rather than from the earlier raw launch/decision.  Full
    // top-level RC extraction showed that a raw-event guard could expire before
    // the delayed register edge: on the MSB trial cmp_fire then rose while the
    // top-plate differential was still moving by hundreds of millivolts.  The
    // acknowledged event therefore clears settle_ready at the DAC update; its
    // return-to-zero tail re-arms the comparator only after that update.
    assign guard_request = sar_event;
    sar_delay_interbit_sg13g2 u_interbit_delay (
        .A(guard_request),
        .X(guard_request_delayed)
    );
    assign guard_set   = guard_request_delayed & ~guard_request & busy;
    assign guard_reset = ~rst_n | ~busy | guard_request;
    sar_async_sr_latch_sg13g2 u_settle_latch (
        .set(guard_set),
        .reset(guard_reset),
        .q(settle_ready)
    );

    // The event register bank is clocked only by the mutually-exclusive
    // launch pulse or a valid StrongARM decision.  This is a local handshake
    // event, not a periodic bit clock.
    always_ff @(posedge sar_event or negedge rst_n) begin
        if (!rst_n) begin
            busy       <= 1'b0;
            done       <= 1'b0;
            code_reg   <= '1;
            active_reg <= '0;
            result     <= '0;
        // ``busy`` is stable throughout the launch pulse, unlike using that
        // same pulse as both the D-mux select and the DFF clock.  The latter
        // raced after P&R and failed to load the one-hot MSB token in PEX.
        end else if (!busy) begin
            busy       <= 1'b1;
            done       <= 1'b0;
            code_reg   <= MSB_MASK;
            active_reg <= MSB_MASK;
        // Once busy is set, every subsequent sar_event edge can only have
        // originated from a completed comparator decision.  Do not re-test
        // the undelayed decision_event level here: the physical event-clock
        // delay intentionally moves the DFF edge beyond that pulse, and using
        // the expired level as a mux select prevented the token from shifting
        // in full-RC PEX.  busy remains stable across the complete conversion
        // and is therefore the safe asynchronous phase discriminator.
        end else begin
            code_reg <= active_reg[0]
                        ? resolved_code
                        : (resolved_code | (active_reg >> 1));
            if (active_reg[0]) begin
                busy       <= 1'b0;
                done       <= 1'b1;
                active_reg <= '0;
                result     <= resolved_code;
            end else begin
                active_reg <= active_reg >> 1;
                done       <= 1'b0;
            end
        end
    end

    assign resolved_code = cmp_decision_hold
                           ? code_reg
                           : (code_reg & ~active_reg);

    // Existing analog-core polarity contract.  The two rows are forced high
    // while the footers are open, including the full physical hold interval.
    assign sample      = track & ~busy;
    assign hold_req    = busy;
    assign dac_code    = busy ? code_reg  : {N{1'b1}};
    assign dac_code_n  = busy ? ~code_reg : {N{1'b1}};
    assign bit_active  = busy ? active_reg : '0;

    // VALID immediately drops fire; the SR acknowledgement permits the next
    // evaluation only after the real delay-cell chain has completed.
    // Interlock evaluation with the physical DAC-register event itself.  The
    // settle SR latch needs finite gate delay to clear at sar_event rising;
    // without this term cmp_fire can glitch high at the code-update edge and
    // evaluate the same trial twice in extracted transistor simulation.
    assign cmp_fire = busy & settle_ready & ~event_pending & ~sar_event
                      & ~cmp_valid & ~cmp_fault;
endmodule
