#!/bin/sh
set -eu

cat <<EOF > /etc/serf/serf.json
{
  "bind": "0.0.0.0:7946",
  "rpc_addr": "0.0.0.0:7373"
}
EOF

serf agent -config-file /etc/serf/serf.json
