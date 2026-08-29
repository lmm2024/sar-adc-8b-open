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
KLU = "klu" in sys.argv[4:]
MERGE = "merge" in sys.argv[4:]
DCIN = [a for a in sys.argv[4:] if a.startswith("dc=")]
STAIR = [a for a in sys.argv[4:] if a.startswith("stair=")]
PAIRS = [a for a in sys.argv[4:] if a.startswith("pairs=")]
SCH = "sch" in sys.argv[4:]
INJ = [a for a in sys.argv[4:] if a.startswith("inj=")]
PEXF = [a for a in sys.argv[4:] if a.startswith("pex=")]

STD = "/foss/pdks/ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice"
LOGIC = "/foss/designs/sar-adc/logic/final/spice/sar_ctrl.spice"
ACORE = "/foss/designs/sar-adc/power/acore12_sch.spice" if "sch" in sys.argv[4:] else ([a[4:] for a in sys.argv[4:] if a.startswith("pex=")] or ["/foss/designs/sar-adc/layout/pex_a13/oa_sar8_acore13.pex.spice"])[0]

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
aports = re.search(r"\.subckt oa_sar8_acore13 ([^\n]*)", ac).group(1).split()
if INJ:
    extra = open(INJ[0][4:]).read().strip()
    lines = ac.split("\n")
    j = next(i for i, ln in enumerate(lines) if ln.startswith(".subckt oa_sar8_acore13"))
    k = next(i for i in range(j, len(lines)) if lines[i].strip().startswith(".ends"))
    lines = lines[:k] + [extra] + lines[k:]
    ac = "\n".join(lines)
    print("injected:", extra.replace(chr(10), " | "))
if MERGE:
    lines = ac.split("\n"); keep = []; caps = {}
    for ln in lines:
        m = re.match(r"^X\S+\s+(\S+)\s+(\S+)\s+cap_cmim\s+l=([0-9.]+)u\s+w=([0-9.]+)u", ln)
        if m:
            a, b, l, w = m.group(1), m.group(2), float(m.group(3)), float(m.group(4))
            key = (a, b, l, w); caps[key] = caps.get(key, 0) + 1
        else:
            keep.append(ln)
    ins = "\n".join(f"XCM{i} {a} {b} cap_cmim l={l}u w={w}u m={n}" for i, ((a, b, l, w), n) in enumerate(caps.items()))
    j = next(i for i, ln in enumerate(keep) if ln.startswith(".subckt oa_sar8_acore13"))
    k = next(i for i in range(j, len(keep)) if keep[i].strip().startswith(".ends"))
    keep = keep[:k] + [ins] + keep[k:]
    ac = "\n".join(keep)
    print("merged cmim instances into", len(caps))
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

def stair_src():
    if PAIRS:
        prs = [tuple(float(x) for x in p.split(":")) for p in PAIRS[0][6:].split(",")]
        lv = [(vp - vn) for vp, vn in prs]
        cm = [(vp + vn) / 2 for vp, vn in prs]
    else:
        lv = [float(v) for v in STAIR[0][6:].split(",")]
        cm = [0.75] * len(lv)
    def pwl(sign):
        pts = []
        t = 0.0
        for i, D in enumerate(lv):
            v = cm[i] + sign * D / 2
            if i == 0:
                pts += [(0.0, v)]
            else:
                t0 = 80e-9 + 200e-9 * (i - 1)
                pts += [(t0, prev), (t0 + 1e-9, v)]
            prev = v
        pts += [(2e-6, prev)]
        return " ".join(f"{a:.10g} {b:.6g}" for a, b in pts)
    return "Vinp vinp 0 pwl(" + pwl(+1) + ")\nVinn vinn 0 pwl(" + pwl(-1) + ")"

tb = f"""* OA-SAR8 mixed-signal post-layout core testbench (analog PEX + digital gate-level)
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib /foss/pdks/ihp-sg13g2/libs.tech/ngspice/models/cornerCAP.lib cap_typ
.option abstol=1e-12 reltol=1e-3 vntol=1e-6 chgtol=1e-14 method=gear{" klu" if KLU else ""}
.param vdd=1.5 amp=0.7 fin=312.5k

{std}
{lgj}
{ac}

VDD vdd 0 {{vdd}}
VCM vcm 0 0.75
{stair_src() if (STAIR or PAIRS) else (("Vinp vinp 0 dc " + str(0.75 + float(DCIN[0][3:])/2) + chr(10) + "Vinn vinn 0 dc " + str(0.75 - float(DCIN[0][3:])/2)) if DCIN else ("Vinp vinp 0 dc 0.75 sin(0.75 {{amp}} {{fin}} 0 0 " + PHASE + ")" + chr(10) + "Vinn vinn 0 dc 0.75 sin(0.75 {{-amp}} {{fin}} 0 0 " + PHASE + ")"))}
* 110 MHz clock: 11 clocks per conversion = 100 ns = 10 MS/s
Vclk clk 0 pulse(0 {{vdd}} 0 0.1n 0.1n 4.4454n 9.0909n)
Vrst rst_n 0 pwl(0 0 30n 0 30.5n {{vdd}})
* start pulses every 100 ns (10 MS/s), each 10 ns wide, first at 45 ns
Vst start 0 pulse(0 {{vdd}} 45n 0.1n 0.1n 9.0909n 100n)

Xacore {' '.join(ac_conn(p) for p in aports)} oa_sar8_acore13
Xlogic {' '.join(lg_conn(p) for p in ports)} sar_ctrl
Cload_r0 result0 0 5f
Cload_r1 result1 0 5f
Cload_r2 result2 0 5f
Cload_r3 result3 0 5f
Cload_r4 result4 0 5f
Cload_r5 result5 0 5f
Cload_r6 result6 0 5f
Cload_r7 result7 0 5f

.save v(done) v(result7) v(result6) v(result5) v(result4) v(result3) v(result2) v(result1) v(result0) v(trk) v(hold) v(vinp) v(vinn) i(VDD) v(outp) v(outn) v(clk_cmp) v(xacore.sw_tg_0.bot) v(xacore.cdac_array_1.topp)
.control
set filetype=ascii
tran 0.2n {TSTOP} uic
meas tran iavg AVG i(VDD) from=200n to={TSTOP}
echo "TOTAL_CORE_IAVG_A = $&iavg"
wrdata /foss/designs/sar-adc/power/mixed6lf{TAG}_out.csv v(done) v(result7) v(result6) v(result5) v(result4) v(result3) v(result2) v(result1) v(result0) v(trk) v(hold) v(vinp) v(vinn) i(VDD) v(outp) v(outn) v(clk_cmp) v(xacore.sw_tg_0.bot) v(xacore.cdac_array_1.topp)
quit
.endc
.end
"""
open(f"/foss/designs/sar-adc/power/tb_mixed6lf{TAG}.spice", "w").write(tb)
print(f"tb_mixed6lf{TAG}.spice written", len(tb) // 1024, "KB")
