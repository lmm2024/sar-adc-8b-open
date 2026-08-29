###############################################################################
# Created by write_sdc
###############################################################################
current_design sar_ctrl_async_phys
###############################################################################
# Timing Constraints
###############################################################################
create_clock -name track -period 47.6190 [get_ports {track}]
set_propagated_clock [get_clocks {track}]
set_input_delay 0.5000 -clock [get_clocks {track}] -add_delay [get_ports {cmp_n}]
set_input_delay 0.5000 -clock [get_clocks {track}] -add_delay [get_ports {cmp_p}]
set_input_delay 0.5000 -clock [get_clocks {track}] -add_delay [get_ports {rst_n}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[0]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[1]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[2]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[3]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[4]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[5]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[6]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {bit_active[7]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {busy}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {cmp_fault}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {cmp_fire}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {cmp_valid}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[0]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[1]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[2]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[3]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[4]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[5]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[6]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code[7]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[0]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[1]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[2]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[3]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[4]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[5]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[6]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {dac_code_n[7]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {done}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {hold_req}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[0]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[1]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[2]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[3]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[4]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[5]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[6]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {result[7]}]
set_output_delay 1.0000 -clock [get_clocks {track}] -add_delay [get_ports {sample}]
set_false_path\
    -from [get_ports {rst_n}]
###############################################################################
# Environment
###############################################################################
###############################################################################
# Design Rules
###############################################################################
