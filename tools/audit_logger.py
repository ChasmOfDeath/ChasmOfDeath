#!/usr/bin/env python3
class AuditLogger:

from datetime import datetime
import os
import json
    def log_activity(self, tool_name, target, user_consent):

        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.log_file = log_file
    def __init__(self, log_file="logs/osint_audit.log"):
            "consent_given": user_consent
            "target": target,
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
        log_entry = {
    print("Audit logger initialized")
    logger = AuditLogger()
