// Physical delay macros for the OA-SAR8 self-timed controller.
//
// There are deliberately no Verilog # delays in this file.  Each delay is a
// chain of real IHP SG13G2 standard cells, so LibreLane can retain, place and
// route the same circuit that creates the delay in silicon.  The initial tap
// counts target the present 1.5 V TT requirements:
//
//   hold path     : 4 x dlygate4sd3 (library description: ~0.7 ns/cell)
//   inter-bit path: 3 x dlygate4sd3 used as a request trailing-edge guard
//   pulse width   : 4 x dlygate4sd3 (PEX-calibrated launch pulse)
//
// The nominal descriptions are not sign-off numbers.  After P&R, the tap
// counts must be selected from extracted TT/1.5 V simulations, then checked at
// the required PVT corners.  Keeping the chains in named modules makes that
// calibration a one-line structural change rather than a control-logic edit.

`timescale 1ns / 1ps

module sar_delay_hold_sg13g2 (
    input  logic A,
    output logic X
);
    (* keep = "true" *) logic t0, t1, t2;
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d0 (.X(t0), .A(A));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d1 (.X(t1), .A(t0));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d2 (.X(t2), .A(t1));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d3 (.X(X),  .A(t2));
endmodule

module sar_delay_interbit_sg13g2 (
    input  logic A,
    output logic X
);
    (* keep = "true" *) logic t0, t1;
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d0 (.X(t0), .A(A));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d1 (.X(t1), .A(t0));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d2 (.X(X),  .A(t1));
endmodule

// Give comparator data and the launch-state mux a real setup interval before
// the shared event register bank sees its active edge.  This is a physical
// clock-path element, not a behavioural delay.
module sar_delay_event_clock_sg13g2 (
    input  logic A,
    output logic X
);
    (* keep = "true" *) logic t0;
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d0 (.X(t0), .A(A));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d1 (.X(X),  .A(t0));
endmodule

module sar_delay_pulsewidth_sg13g2 (
    input  logic A,
    output logic X
);
    // The former single sd1 cell produced a pulse that was visible in RTL/SDF
    // but was completely filtered by the post-route transistor network: the
    // shared event-clock pin reached only millivolts.  Four sd3 cells give the
    // launch event roughly the same 1.3 ns TT/1.5 V PEX separation measured
    // across the hold chain, wide enough for the physical DFF bank while
    // remaining far below one asynchronous bit cycle.
    (* keep = "true" *) logic t0, t1, t2;
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d0 (.X(t0), .A(A));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d1 (.X(t1), .A(t0));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d2 (.X(t2), .A(t1));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_dlygate4sd3_1 u_d3 (.X(X),  .A(t2));
endmodule

// Active-high cross-coupled-NOR SR latch.  This is used only for the settling
// acknowledgement; reset and set are qualified so they cannot be high in the
// intended protocol.  Instantiating real cells avoids inferred behavioral
// storage and makes the feedback loop explicit to LVS.
module sar_async_sr_latch_sg13g2 (
    input  logic set,
    input  logic reset,
    output logic q
);
    (* keep = "true" *) logic q_n;
    (* keep = "true", dont_touch = "true" *)
    sg13g2_nor2_1 u_q  (.Y(q),   .A(reset), .B(q_n));
    (* keep = "true", dont_touch = "true" *)
    sg13g2_nor2_1 u_qn (.Y(q_n), .A(set),   .B(q));
endmodule
