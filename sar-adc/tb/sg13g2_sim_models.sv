// Minimal behavioral models of the PDK cells instantiated directly in RTL
// (RTL simulation only; synthesis binds the real liberty cells).
`timescale 1ns / 1ps
module sg13g2_nand2_1 (output logic Y, input logic A, input logic B);
    assign #0.03 Y = ~(A & B);
endmodule
