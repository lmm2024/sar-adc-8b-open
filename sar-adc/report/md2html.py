#!/usr/bin/env python3
"""Minimal Markdown -> standalone HTML (tables, headings, lists, bold, code, images inlined as base64)."""
import re, base64, html, sys, os

src = open("OA-SAR8_设计报告.md", encoding="utf-8").read()
imgdir = "img"

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t

out = []
lines = src.split("\n")
i = 0
in_list = False
while i < len(lines):
    ln = lines[i]
    if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-|:]+\|$", lines[i + 1]):
        hdr = [c.strip() for c in ln.strip("|").split("|")]
        i += 2
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip("|").split("|")])
            i += 1
        out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in hdr) + "</tr></thead><tbody>")
        for r in rows:
            out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
        out.append("</tbody></table>")
        continue
    if in_list and not re.match(r"^\s*(-|\d+\.)\s", ln):
        out.append("</ul>" if in_list == "ul" else "</ol>")
        in_list = False
    m = re.match(r"^(#+)\s+(.*)", ln)
    if m:
        lvl = len(m.group(1))
        out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
    elif ln.strip() == "---":
        out.append("<hr>")
    elif re.match(r"^\s*-\s", ln):
        if in_list != "ul":
            out.append("<ul>"); in_list = "ul"
        out.append(f"<li>{inline(re.sub(r'^\s*-\s', '', ln))}</li>")
    elif re.match(r"^\s*\d+\.\s", ln):
        if in_list != "ol":
            out.append("<ol>"); in_list = "ol"
        out.append(f"<li>{inline(re.sub(r'^\s*\d+\.\s', '', ln))}</li>")
    elif ln.strip():
        out.append(f"<p>{inline(ln)}</p>")
    i += 1
if in_list:
    out.append("</ul>" if in_list == "ul" else "</ol>")

# figure gallery appended
figs = sorted(f for f in os.listdir(imgdir) if f.endswith(".png"))
gallery = ["<hr><h2>附图：版图截图</h2>"]
for f in figs:
    b64 = base64.b64encode(open(os.path.join(imgdir, f), "rb").read()).decode()
    gallery.append(f'<figure><img src="data:image/png;base64,{b64}" style="max-width:100%"><figcaption>{f}</figcaption></figure>')

css = """body{font-family:-apple-system,'PingFang SC','Noto Sans CJK SC',sans-serif;max-width:1000px;margin:40px auto;padding:0 20px;line-height:1.6;color:#222}
table{border-collapse:collapse;margin:12px 0;font-size:14px}th,td{border:1px solid #bbb;padding:6px 10px;text-align:left;vertical-align:top}th{background:#f0f0f0}
code{background:#f4f4f4;padding:1px 4px;border-radius:3px;font-size:13px}h1{border-bottom:2px solid #333}h2{border-bottom:1px solid #999;margin-top:36px}
figure{margin:24px 0}figcaption{font-size:13px;color:#555}"""
doc = f"<!DOCTYPE html><html lang='zh'><head><meta charset='utf-8'><title>OA-SAR8 芯片设计报告</title><style>{css}</style></head><body>" + "\n".join(out + gallery) + "</body></html>"
open("OA-SAR8_设计报告.html", "w", encoding="utf-8").write(doc)
print("html written", len(doc) // 1024, "KB;", len(figs), "figures embedded")
