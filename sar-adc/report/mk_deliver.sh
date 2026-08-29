#!/bin/bash
# Rebuild the v2 deliverables: screenshots zip (3 categories) + report md/html + spec + chip GDS
set -e
cd /Users/tokenzhang/open-analog/designs/sar-adc/report
rm -rf zipwork && mkdir -p zipwork/1_modules zipwork/2_core zipwork/3_full_chip
cp img/0[1-6]_*.png zipwork/1_modules/
cp img/07_*.png img/08_*.png zipwork/2_core/
cp img/09_*.png img/10_*.png img/11_*.png zipwork/3_full_chip/
rm -f OA-SAR8_layout_screenshots.zip
(cd zipwork && zip -qr ../OA-SAR8_layout_screenshots.zip 1_modules 2_core 3_full_chip)
python3 md2html.py
mkdir -p deliver
cp OA-SAR8_设计报告.md OA-SAR8_设计报告.html OA-SAR8_layout_screenshots.zip deliver/
cp ../docs/spec.md deliver/OA-SAR8_spec_v0.2.md 2>/dev/null || true
cp ../../sar-chip/layout/chip_top.gds.gz deliver/chip_top.gds.gz
rm -f OA-SAR8_交付包.zip
(cd deliver && zip -q ../OA-SAR8_交付包.zip OA-SAR8_设计报告.md OA-SAR8_设计报告.html OA-SAR8_spec_v0.2.md OA-SAR8_layout_screenshots.zip chip_top.gds.gz)
ls -la OA-SAR8_交付包.zip OA-SAR8_layout_screenshots.zip
