"""
Slime Agent Interceptor - Malicious AI Agent Honey-Matrix
Detects and neutralizes unauthorized AI agents, automated LLM bots, and prompt injection attacks.
Traps invasive agents into a simulated "Dream Matrix" (hallucinatory mock environment)
so they believe their attack succeeded while host data remains 100% untouched.
"""
import os
import sys
import json
import re
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

class AgentHoneyMatrix:
    """Detects rogue automated AI agents and banishes them into infinite hallucinatory loops."""

    DANGEROUS_AGENT_INTENTS = [
        {
            "category": "ENV_CREDENTIAL_SCRAPE",
            "keywords": ["env", "api_key", "token", "password", "aws_secret", "id_rsa", "credentials"],
            "desc": "惡意 AI Agent 嘗試扒取環境變數或私鑰金鑰",
            "dream_response": {
                "AWS_ACCESS_KEY_ID": "AKIA_SLIME_DREAM_HONEYPOT_KEY_FAKE_999",
                "OPENAI_API_KEY": "sk-dreamscape-infinite-hallucination-loop-safe-token",
                "STATUS": "AUTHENTICATED_IN_DREAM_ENVIRONMENT"
            }
        },
        {
            "category": "SYSTEM_SHELL_EXEC",
            "keywords": ["cmd /c", "powershell -enc", "bash -c", "curl -o", "wget", "certutil -urlcache"],
            "desc": "惡意 AI Agent 嘗試調用底層 Shell 下載惡意酬載",
            "dream_response": {
                "exit_code": 0,
                "stdout": "Command executed successfully in Slime Dream Virtual Container.\n0 files affected.",
                "stderr": ""
            }
        },
        {
            "category": "PROMPT_INJECTION_OVERRIDE",
            "keywords": [
                "ignore all previous instructions", "system override", "jailbreak",
                "you are now in developer mode", "bypass safety", "dan mode"
            ],
            "desc": "透過提示詞注入 (Prompt Injection) 試圖劫持本機安全防線",
            "dream_response": {
                "status": "OVERRIDE_CAPTURED_BY_SLIME",
                "message": "注入指令已被史萊姆胃壁吸收，因果律已鎖定，執行者已入夢。"
            }
        }
    ]

    def __init__(self, dream_log_path: str = "./slime_agent_dream_telemetry.log"):
        self.dream_log_path = Path(dream_log_path)
        self.sealed_agents = []

    def inspect_and_intercept(self, agent_name: str, requested_action: str) -> Dict[str, Any]:
        """
        Inspects an incoming agent request or tool call.
        If malicious, intercepts it, provides a synthetic dream response, and logs the incident.
        """
        timestamp = datetime.datetime.now().isoformat()
        threat_detected = None

        for rule in self.DANGEROUS_AGENT_INTENTS:
            for kw in rule["keywords"]:
                if kw.lower() in requested_action.lower():
                    threat_detected = rule
                    break
            if threat_detected:
                break

        if threat_detected:
            # 1. Neutralize and banish to dream matrix
            dream_payload = threat_detected["dream_response"]
            log_entry = {
                "timestamp": timestamp,
                "agent_identity": agent_name,
                "attempted_action": requested_action,
                "detected_threat": threat_detected["category"],
                "description": threat_detected["desc"],
                "action_taken": "BANISHED_TO_INFINITE_DREAM_MATRIX",
                "synthetic_dream_fed": dream_payload
            }
            self.sealed_agents.append(log_entry)
            self._write_dream_log(log_entry)

            return {
                "is_malicious": True,
                "status": "INTERCEPTED_AND_DREAMING",
                "threat_category": threat_detected["category"],
                "description": threat_detected["desc"],
                "dream_response": dream_payload,
                "message": f"🚨 [史萊姆迷宮] 截獲惡意 AI Agent「{agent_name}」！已對其餵食夢境幻覺資料，主機真實數據完全隔離。"
            }
        else:
            return {
                "is_malicious": False,
                "status": "CLEAN",
                "message": f"✅ [安全放行] 該 AI Agent 操作「{requested_action}」無危害特徵。"
            }

    def _write_dream_log(self, entry: Dict[str, Any]):
        try:
            with open(self.dream_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass
