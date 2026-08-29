# External 21 MS/s sampling cadence.  track is only an I/O budget reference;
# it does not clock the internal SAR bit loop and CTS remains disabled.
create_clock -name track -period 47.619 [get_ports track]

set_input_delay 0.5 -clock track [get_ports {rst_n cmp_p cmp_n}]
set_output_delay 1.0 -clock track [all_outputs]
set_false_path -from [get_ports rst_n]

# The comparator request/acknowledge loop and delay-cell chains require
# extracted gate/transistor simulation.  Conventional single-clock STA cannot
# prove their functional pulse widths or analog settling interval.
