#!/usr/bin/env python3
"""
Append a timestamped task entry to AGENT_LOG.md

Usage:
    python tools/log_task.py "Task message" [status]
Status defaults to 'done', or provide 'in-progress', 'todo', 'failed'.
"""
import sys
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(ROOT, 'AGENT_LOG.md')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: log_task.py "message" [status]')
        sys.exit(1)
    msg = sys.argv[1]
    status = sys.argv[2] if len(sys.argv) > 2 else 'done'
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')
    entry = f'- [{ts}] ({status}) {msg}\n'
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'w', encoding='utf-8') as f:
            f.write('# AGENT LOG - incremental updates\n\n')
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(entry)
    print('Logged:', entry.strip())
