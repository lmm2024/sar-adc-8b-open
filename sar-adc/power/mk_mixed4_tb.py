#!/usr/bin/env python3
"""Build the mixed-signal, transistor-level, post-layout testbench of the whole
core: analog core = PEX netlist (all devices + 567 parasitic C), digital = LibreLane
gate-level spice of sar_ctrl on the stdcell CDL (transistor level). One VDD source,
real clk/start/rst_n, differential sine input, closed loop. Measures conversion codes
and average supply current at 10 MS/s."""
import re, sys
TSTOP = sys.argv[1] if len(sys.argv) > 1 else "3600n"
PHASE = sys.argv[2] if len(sys.argv) > 2 else "0"
TAG = sys.argv[3] if len(sys.argv) > 3 else ""

STD = "/foss/pdks/ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice"
LOGIC = "/foss/designs/sar-adc/logic/final/spice/sar_ctrl.spice"
ACORE = "/foss/designs/sar-adc/layout/pex_a12/oa_sar8_acore12.pex.spice"

# --- stdcell CDL -> ngspice: strip parameters ngspice dislikes, keep subckts as-is (rfmode etc. fine)
std = open(STD).read()
# --- logic spice: join continuation lines, drop black-box abstract subckts
lg = open(LOGIC).read().split("\n")
joined = []
for ln in lg:
    if ln.startswith("+") and joined:
        joined[-1] += " " + ln[1:].strip()
    else:
        joined.append(ln)
lgj = "\n".join(joined)
lgj = re.sub(r"\* Black-box entry subcircuit for \S+ abstract view\n\.subckt \S+[^\n]*\n\.ends\n", "", lgj)
ports = re.search(r"\.subckt sar_ctrl ([^\n]*)", lgj).group(1).split()
print("logic ports:", ports)

# --- analog core pex: substrate node 'sub' -> 0 ; find its port list
ac_lines = open(ACORE).read().replace(" sub ", " 0 ").split("\n")
acj = []
for ln in ac_lines:
    if ln.startswith("+") and acj:
        acj[-1] += " " + ln[1:].strip()
    else:
        acj.append(ln)
ac = "\n".join(acj)
aports = re.search(r"\.subckt oa_sar8_acore12 ([^\n]*)", ac).group(1).split()
print("acore ports:", aports)

def lg_conn(p):
    m = {f"dac_code[{k}]": f"ctl{k}n" for k in range(8)}      # FIX-B: P array gets the complement (inverting drivers)
    m.update({f"dac_code_n[{k}]": f"ctl{k}" for k in range(8)})
    m.update({"cmp": "outp", "cmp_n": "outn", "clk_cmp": "clk_cmp", "sample": "trk", "hold": "hold", "clk": "clk", "VDD": "vdd", "VSS": "0",
              "rst_n": "rst_n", "start": "start", "busy": "busy", "done": "done"})
    m.update({f"result[{k}]": f"result{k}" for k in range(8)})
    return m.get(p, p)

def ac_conn(p):
    m = {"VDD": "vdd", "VSS": "0", "vinp": "vinp", "vinn": "vinn", "vcm": "vcm", "clk_cmp": "clk_cmp",
         "trk": "trk", "hold": "hold", "outp": "outp", "outn": "outn"}
    return m.get(p, p)

tb = f"""* OA-SAR8 mixed-signal post-layout core testbench (analog PEX + digital gate-level)
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerCAP.lib cap_typ
.option abstol=1e-13 reltol=1e-3 vntol=1e-6 chgtol=1e-16 method=gear
.param vdd=1.5 amp=0.7 fin=4.6875meg

{std}
{lgj}
{ac}

VDD vdd 0 {{vdd}}
VCM vcm 0 0.75
Vinp vinp 0 dc 0.75 sin(0.75 {{amp}} {{fin}} 0 0 {PHASE})
Vinn vinn 0 dc 0.75 sin(0.75 {{-amp}} {{fin}} 0 0 {PHASE})
* 110 MHz clock: 11 clocks per conversion = 100 ns = 10 MS/s
Vclk clk 0 pulse(0 {{vdd}} 0 0.1n 0.1n 4.4454n 9.0909n)
Vrst rst_n 0 pwl(0 0 30n 0 30.5n {{vdd}})
* start pulses every 100 ns (10 MS/s), each 10 ns wide, first at 45 ns
Vst start 0 pulse(0 {{vdd}} 45n 0.1n 0.1n 9.0909n 100n)

Xacore {' '.join(ac_conn(p) for p in aports)} oa_sar8_acore12
Xlogic {' '.join(lg_conn(p) for p in ports)} sar_ctrl
Cload_r0 result0 0 5f
Cload_r1 result1 0 5f
Cload_r2 result2 0 5f
Cload_r3 result3 0 5f
Cload_r4 result4 0 5f
Cload_r5 result5 0 5f
Cload_r6 result6 0 5f
Cload_r7 result7 0 5f

.save v(done) v(result7) v(result6) v(result5) v(result4) v(result3) v(result2) v(result1) v(result0) v(trk) v(hold) v(vinp) v(vinn) i(VDD) v(outp) v(outn) v(clk_cmp)
.control
set filetype=ascii
tran 0.05n {TSTOP} uic
meas tran iavg AVG i(VDD) from=200n to={TSTOP}
echo "TOTAL_CORE_IAVG_A = $&iavg"
wrdata /foss/designs/sar-adc/power/mixed4{TAG}_out.csv v(done) v(result7) v(result6) v(result5) v(result4) v(result3) v(result2) v(result1) v(result0) v(trk) v(hold) v(vinp) v(vinn) i(VDD) v(outp) v(outn) v(clk_cmp)
quit
.endc
.end
"""
open(f"/foss/designs/sar-adc/power/tb_mixed4{TAG}.spice", "w").write(tb)
print(f"tb_mixed4{TAG}.spice written", len(tb) // 1024, "KB")
