#!/usr/bin/env python3
# same as fft_mixed_seg.py but for the 312.5 kHz (bin 1) run: files mixed4lf_s*_out.csv
import runpy, sys
sys.argv = ['fft_mixed_seg.py']
src = open('/foss/designs/sar-adc/power/fft_mixed_seg.py').read()
src = src.replace('mixed4_s{}_out.csv', 'mixed4lf_s{}_out.csv').replace('NFFT, BIN, FS, VDD = 32, 15, 10e6, 1.5', 'NFFT, BIN, FS, VDD = 32, 1, 10e6, 1.5')
exec(compile(src, 'fft_mixed_seg_lf', 'exec'))
