#!/usr/bin/env bash
# Run a command inside the IIC-OSIC-TOOLS container (login shell so PATH is complete).
#   tools/run.sh sar-adc/rtl "iverilog -g2012 -o /tmp/t.vvp ../tb/tb_sar_ctrl.sv ../tb/sg13g2_sim_models.sv sar_ctrl.sv && vvp /tmp/t.vvp"
# The repository root must be mounted at /foss/designs inside the container.
CONTAINER="${CONTAINER:-iic-osic-tools_xvnc_uid_$(id -u)}"
DIR="$1"; shift
exec docker exec "$CONTAINER" bash -lc "cd /foss/designs/${DIR} && $*"
