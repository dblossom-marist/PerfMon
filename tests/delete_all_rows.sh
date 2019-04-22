#!/bin/bash
sqlite3 MetricCollector.db << EOF
 delete from all_cpus;
 delete from all_cpus_avg;
 delete from memory_percent;
 delete from per_cpu_percent;
 delete from processes;
EOF
