#!/bin/bash

# .devcontainer/project-feature/install.sh: Install step of the project-owned devcontainer feature
#
# Installs the Antigravity CLI (agy) into /usr/local/bin during container image build.

set -euo pipefail

REMOTE_USER="${_REMOTE_USER:-vscode}"

curl -fsSL https://antigravity.google/cli/install.sh | bash -s -- --dir /usr/local/bin

if id "$REMOTE_USER" >/dev/null 2>&1 && [[ -f /usr/local/bin/agy ]]; then
    chown "$REMOTE_USER:$REMOTE_USER" /usr/local/bin/agy
fi

rm -rf /root/.cache/antigravity
