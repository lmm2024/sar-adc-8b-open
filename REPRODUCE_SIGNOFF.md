# Reproduce the current core18 sign-off

## 1. Start the portable environment

Use `docker.io/hpretl/iic-osic-tools:2026.07`, mount the repository at `/foss/designs`, and run commands through a login shell. The PDK is expected at `/foss/pdks/ihp-sg13g2` inside the container; see `ENVIRONMENT.md`.

```bash
docker run -d --name iic-sar \
  -v "$PWD:/foss/designs" \
  hpretl/iic-osic-tools:2026.07 tail -f /dev/null
docker exec iic-sar bash -lc 'cd /foss/designs/sar-adc && ngspice -v'
```

## 2. Verify the checked-in physical views

The exact sign-off inputs are:

```text
layout/oa_sar8_core18_final.gds
layout/core18_final_full.cdl
layout/pex_core18_final_w2_rc/oa_sar8_core18_final.pex.spice
logic/runs/RUN_2026-08-20_POSTDAC_PENDING/final/gds/sar_ctrl_async_phys.gds
```

Do not regenerate or overwrite these files before reproducing the recorded result.

## 3. Run the 10 MS/s PEX ENOB test

```bash
cd /foss/designs/sar-adc
python3 postlayout/run_core18_pex.py \
  --fs-msps 10 --track-ns 25 --samples 33 \
  --fft-points 32 --tone-bin 15 --amplitude 0.70 \
  --tstep-ns 0.05 --tag repro_10m
```

The generated files are written under `postlayout/build/core18_pex/`. The result should contain 33 completed samples and an ENOB close to 7.9643 bit. Compare with `results/core18_pex/metrics_exact_repro_10m_signoff.json`.

## 4. Optional speed A/B tests

Keep every option unchanged except `--fs-msps` and `--track-ns`:

```bash
python3 postlayout/run_core18_pex.py --fs-msps 10.5 --track-ns 25 --samples 33 --fft-points 32 --tone-bin 15 --amplitude 0.70 --tstep-ns 0.05 --tag repro_10p5_track25
python3 postlayout/run_core18_pex.py --fs-msps 10.5 --track-ns 30 --samples 33 --fft-points 32 --tone-bin 15 --amplitude 0.70 --tstep-ns 0.05 --tag repro_10p5_track30
```

These are exploratory results and are not accepted as sign-off unless the ENOB target is met with the full 33-sample record.

## 5. Regenerate layout and PEX (optional)

```bash
cd /foss/designs/sar-adc/layout
klayout -zz -r gen_acore18_opt.py
klayout -zz -r gen_core18_final.py
sak-drc.sh -k -w drc_core18 oa_sar8_core18_final
sak-lvs.sh -k -w lvs_core18 -s core18_final_full.cdl -l oa_sar8_core18_final.gds -c oa_sar8_core18_final
sak-pex.sh -k -w pex_core18 oa_sar8_core18_final
```

After any physical change, DRC, LVS, PEX and the 10 MS/s ENOB regression must all be rerun. The checked-in GDS/PEX remain the reference sign-off artifacts.
