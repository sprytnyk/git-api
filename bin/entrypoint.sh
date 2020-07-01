#!/bin/bash
# create pdb++ config
cat > ~/.pdbrc.py <<EOF
import pdb


class Config(pdb.DefaultConfig):
    sticky_by_default = True
    truncate_long_lines = False
EOF

# run backend container
gunicorn -b 0.0.0.0:5005 --worker-class eventlet \
--log-level CRITICAL --reload --timeout 600 "manage:app"
