read_liberty /foss/pdks/ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p50V_25C.lib
read_verilog /foss/designs/sar-adc/logic/runs/RUN_2026-08-15_19-08-09/final/nl/sar_ctrl.nl.v
link_design sar_ctrl
read_spef /foss/designs/sar-adc/logic/runs/RUN_2026-08-15_19-08-09/final/spef/nom/sar_ctrl.nom.spef
create_clock -name clk -period 10 [get_ports clk]
set_input_transition 0.1 [all_inputs]
read_vcd -scope tb_gl_power/dut /foss/designs/sar-adc/power/sar_gl.vcd
report_power
