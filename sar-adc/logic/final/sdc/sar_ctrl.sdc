###############################################################################
# Created by write_sdc
###############################################################################
current_design sar_ctrl
###############################################################################
# Timing Constraints
###############################################################################
create_clock -name clk -period 10.0000 [get_ports {clk}]
set_propagated_clock [get_clocks {clk}]
set_input_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {cmp}]
set_input_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {cmp_n}]
set_input_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {rst_n}]
set_input_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {start}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {busy}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {clk_cmp}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[0]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[1]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[2]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[3]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[4]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[5]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[6]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code[7]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[0]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[1]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[2]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[3]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[4]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[5]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[6]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {dac_code_n[7]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {done}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {hold}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[0]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[1]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[2]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[3]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[4]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[5]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[6]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {result[7]}]
set_output_delay 1.0000 -clock [get_clocks {clk}] -add_delay [get_ports {sample}]
###############################################################################
# Environment
###############################################################################
###############################################################################
# Design Rules
###############################################################################
