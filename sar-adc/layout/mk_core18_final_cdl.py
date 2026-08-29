#!/usr/bin/env python3
"""Build the complete LVS reference for oa_sar8_core18_final."""
from pathlib import Path


src = Path("mk_core17_async_cdl.py").read_text(encoding="utf-8")
src = src.replace('ACORE13 = HERE / "acore13.cdl"',
                  'ACORE13 = HERE / "acore18_opt.cdl"')
src = src.replace('OUT = HERE / "core17_async_full.cdl"',
                  'OUT = HERE / "core18_final_full.cdl"')
src = src.replace("oa_sar8_core17_async", "oa_sar8_core18_final")
src = src.replace("oa_sar8_acore13", "oa_sar8_acore18_opt")
exec(compile(src, "mk_core18_final_cdl.expanded.py", "exec"))
