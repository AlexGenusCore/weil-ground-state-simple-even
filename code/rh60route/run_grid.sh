#!/bin/bash
# Grid G runner (PREREG_GRID.md §4) for ONE VM: memory-safe parallel execution of grid/jobs.txt.
#   run_grid.sh stamp            write ~/rh60route/GRID.stamp once (md5 of the registered documents and every executed file, UTC)
#   run_grid.sh run [JOBS]       run the jobs (default: the registered grid/jobs.txt); needs GRID.stamp
# jobs.txt: "ID GB CPU DEPS CMD..." per line (# = comment). DEPS is a comma list of job IDs or "-"; a job starts once every dep
# has finished (any exit status: jobs check their own inputs). Lines are taken in file order (the order is the priority). Admission:
#   slots:  sum CPU of running jobs + CPU <= SLOTS (default nproc - 4)
#   memory: sum GB of running jobs + GB <= BUDGET = 0.85*MemTotal - (MemTotal - MemAvailable at start)   (15 % headroom)
#           and, live, MemAvailable - GB >= 0.15*MemTotal
# GB is the job's peak-RSS budget (pilot/fixes JSON peaks, +10 %; GRID_PLAN.md §3). Each job runs niced under its own setsid, so
# the watchdog can kill exactly that process group (explicit PGID) if MemAvailable < 5 % of MemTotal; that is a K4g stop.
# Each job also gets oom_score_adj 1000 (a kernel OOM takes a grid job, never sshd or other work), its peak RSS goes to
# logs/ID.rss (GNU time: KB, wall s; R-6g), and the runner samples each job's session RSS every loop: above 1.25 x its budget
# it writes STOP_RSS_ID (K4g, live). An exit status other than 0, 3 or 4 (3/4 = REFINE marker or refinement pending) writes
# STOP_EXIT_ID (K2g: a crash in any job).
# done/ID holds the exit status; jobs.txt is re-read every loop, so refinement jobs may be appended while it runs.
# Nothing new is launched once $RUN/out/STOP_* exists (N2, G2, hard gate, crash, RSS, watchdog); running jobs finish.
set -u
R=$HOME/rh60route; H=$R/hp; G=$H/lb/rh60route/grid; RUN=$R/grid_run
export PY=$HOME/weil/.venv/bin/python R RUN G CODE=$H/lb/rh60route/code LIU_DATA=$R/data
export RH60_RUN=$RUN RH60_STAMP=$R/GRID.stamp RH60_AMEND=$R/AMENDMENTS.log
mkdir -p $RUN/out $RUN/logs $RUN/upper $RUN/glue $RUN/done $RUN/pids $R/data/s $R/work

if [ "${1:-}" = stamp ]; then
  S=$R/GRID.stamp; [ -e $S ] && { echo "stamp exists"; exit 1; }
  # pre-commitment stamp (vm4, grid review): every file it lists must be unchanged unless ALLOW_DIFF=1 after a logged amendment
  if [ -e $R/PREREG_GRID.stamp ]; then
    ( cd $R && grep -E '^[0-9a-f]{64}  ' PREREG_GRID.stamp | sha256sum -c --quiet ) || [ "${ALLOW_DIFF:-0}" = 1 ] || { echo "differs from PREREG_GRID.stamp"; exit 1; }
  fi
  # fill archive/ before any job (F4): concurrent first runs would otherwise race to copy the same new blob
  $PY -I -c "import sys; sys.path.insert(0, '$CODE'); import certify; certify.archive()" || exit 1
  for f in $G/{grid.py,plan.py,forecast.py,run_grid.sh} $H/gap/check_steps.py $H/lb/liu/{stage_s.py,liu.py} $R/upper/{fr_sweep.py,fast_recurrence.py,hp.py}; do
    a=$H/lb/rh60route/archive/$(sha256sum < $f | cut -c1-64).${f##*/}; [ -e $a ] || { cp $f $a && chmod 444 $a; } || exit 1
  done  # executables outside code/ that certify.archive() does not see (F4)
  { echo "# GRID stamp, rh_60-route grid G on [1.4035, 2]"
    [ -e $R/PREREG_GRID.stamp ] && echo "PREREG_GRID.stamp sha256 $(sha256sum < $R/PREREG_GRID.stamp | cut -c1-64) (ALLOW_DIFF=${ALLOW_DIFF:-0})"
    md5sum $H/lb/rh60route/{PREREG_GRID.md,GRID_PLAN.md,SPEC.md,PROOFS.md,review.md,spec_changes.md,PREREG.md,AUDIT.md,FIXES.md}
    md5sum $G/{jobs.txt,windows.txt,run_grid.sh,grid.py,plan.py,forecast.py,forecast.jsonl,forecast_check.jsonl}
    md5sum $CODE/{certify.py,entries.py,eqp.py,indep.py,mp_entries.py,sr.py,sr.c,sr_kernel,g3.py,g4.py,ritz.py,pilot.py,amend.py}
    md5sum $H/lb/liu/{stage_s.py,liu.py} $H/gap/elston/{grid_norm.py,grid_certificate_rigorous.py,progress.py} $H/gap/check_steps.py
    md5sum $R/upper/{fr_sweep.py,fast_recurrence.py,hp.py} $RUN/upper/*.jsonl $R/data/s/*.json $R/data/ritz_*.json
    $PY $CODE/amend.py $R/AMENDMENTS.log --verify
    date -u; } > $S
  chmod 444 $S; cat $S; exit 0
fi
[ "${1:-}" = run ] || { sed -n 2,17p "$0"; exit 1; }
[ -e $RH60_STAMP ] || { echo "no GRID.stamp"; exit 1; }
[ -x /usr/bin/time ] || { echo "needs GNU time (/usr/bin/time) for the RSS records"; exit 1; }
JOBS=${2:-$G/jobs.txt}; SLOTS=${SLOTS:-$(( $(nproc) - 4 ))}
mem() { awk -v k=$1 '$1==k":"{print int($2/1024)}' /proc/meminfo; }   # MB
TOT=$(mem MemTotal); BUDGET=$(( TOT*85/100 - (TOT - $(mem MemAvailable)) ))
echo "$(date -u +%FT%TZ) start: MemTotal ${TOT} MB, budget ${BUDGET} MB, slots $SLOTS, jobs $JOBS" | tee -a $RUN/logs/runner.log

while :; do
  # reap finished jobs; sum what is still running
  USED=0; CPUS=0; NRUN=0
  for p in $RUN/pids/*; do
    [ -e "$p" ] || continue; id=${p##*/}
    if [ -e $RUN/done/$id ]; then rm -f $p; continue; fi
    read pg gb cpu < $p
    kill -0 $pg 2>/dev/null || { [ -e $RUN/done/$id ] || echo 255 > $RUN/done/$id; rm -f $p; continue; }  # wrapper gone
    USED=$(( USED + gb )); CPUS=$(( CPUS + cpu )); NRUN=$(( NRUN + 1 ))
    r=$(ps -o rss= -s $pg 2>/dev/null | awk '{s+=$1} END{print int(s/1024)}')  # MB, the job's whole session (gb holds MB here)
    [ ${r:-0} -gt $(( gb*5/4 )) ] && [ ! -e $RUN/out/STOP_RSS_$id ] && \
      echo "$(date -u +%FT%TZ) $id RSS ${r} MB > 1.25 x budget ${gb} MB (K4g)" | tee -a $RUN/logs/runner.log > $RUN/out/STOP_RSS_$id
  done
  AV=$(mem MemAvailable)
  if [ $NRUN -gt 0 ] && [ $AV -lt $(( TOT*5/100 )) ]; then   # watchdog: kill the most recently started job's process group
    p=$(ls -t $RUN/pids | head -1); read pg gb cpu < $RUN/pids/$p
    echo "$(date -u +%FT%TZ) MemAvailable ${AV} MB < 5%: kill -- -$pg ($p)" | tee -a $RUN/logs/runner.log $RUN/out/STOP_MEM
    kill -- -$pg; echo 137 > $RUN/done/$p; sleep 30; continue
  fi
  STOPPED=$(ls $RUN/out/STOP_* 2>/dev/null | head -1)
  PENDING=0
  while read -r id gb cpu deps cmd; do
    case "$id" in ''|\#*) continue;; esac
    [ -e $RUN/done/$id ] || [ -e $RUN/pids/$id ] && continue
    PENDING=$(( PENDING + 1 )); [ -n "$STOPPED" ] && continue
    ok=1; [ "$deps" = - ] || for d in ${deps//,/ }; do [ -e $RUN/done/$d ] || { ok=0; break; }; done
    [ $ok = 1 ] || continue
    mb=$(awk -v g=$gb 'BEGIN{print int(g*1024+0.5)}')
    [ $mb -le $BUDGET ] && [ $cpu -le $SLOTS ] || { echo 254 > $RUN/done/$id; echo "$(date -u +%FT%TZ) $id can never fit: skipped (254)" >> $RUN/logs/runner.log; continue; }
    [ $(( CPUS + cpu )) -le $SLOTS ] && [ $(( USED + mb )) -le $BUDGET ] && [ $(( AV - mb )) -ge $(( TOT*15/100 )) ] || continue
    setsid bash -c "cd $R; echo 1000 > /proc/self/oom_score_adj 2>/dev/null
      nice -n 5 /usr/bin/time -f '%M %e' -o $RUN/logs/$id.rss bash -c '$cmd' > $RUN/logs/$id.log 2>&1 < /dev/null; rc=\$?
      case \$rc in 0|3|4) ;; *) echo rc \$rc > $RUN/out/STOP_EXIT_$id;; esac; echo \$rc > $RUN/done/$id" &
    echo "$! $mb $cpu" > $RUN/pids/$id
    USED=$(( USED + mb )); CPUS=$(( CPUS + cpu )); AV=$(( AV - mb )); NRUN=$(( NRUN + 1 ))
    echo "$(date -u +%FT%TZ) start $id (pgid $!, ${gb} GB, $cpu cpu; running $NRUN, ${USED} MB)" >> $RUN/logs/runner.log
  done < "$JOBS"
  if [ $NRUN -eq 0 ] && { [ $PENDING -eq 0 ] || [ -n "$STOPPED" ]; }; then
    echo "$(date -u +%FT%TZ) finished: pending $PENDING, stop ${STOPPED:-none}" | tee -a $RUN/logs/runner.log; exit 0
  fi
  sleep 20
done
