# -*- coding: utf-8 -*-
"""Orchestrator：固件（BIOS/AI BIOS）多智能体流水线编排器。"""
from __future__ import annotations

import logging
import time
import uuid
from typing import Any, Dict, List

from . import boot_flow, firmware_security, ai_bios, mainboard_adapt

logger = logging.getLogger(__name__)

AGENT_REGISTRY = {
    "boot_flow": (boot_flow.BootFlowAgent, "固件启动流程（POST/UEFI/OpenFirmware）"),
    "firmware_security": (firmware_security.FirmwareSecurityAgent, "固件安全（Secure Boot/签名/供应链）"),
    "ai_bios": (ai_bios.AIBIOSAgent, "AI BIOS（智能诊断/自适应配置）"),
    "mainboard_adapt": (mainboard_adapt.MainboardAdaptAgent, "主板适配"),
}


class Orchestrator:
    def __init__(self, llm_gateway=None, data_dir=None):
        self.llm_gateway = llm_gateway
        self.data_dir = data_dir
        self._tasks: Dict[str, Dict[str, Any]] = {}

    def plan(self, goal: str) -> List[Dict[str, Any]]:
        g = goal.lower()
        plan: List[Dict[str, Any]] = []
        if any(k in g for k in ["启动", "post", "uefi", "openfirmware", "固件流程", "boot"]):
            plan.append({"agent": "boot_flow", "action": "analyze", "params": {}})
        if any(k in g for k in ["安全", "secure", "签名", "供应链", "投毒", "security"]):
            plan.append({"agent": "firmware_security", "action": "secure_boot", "params": {}})
        if any(k in g for k in ["ai", "智能", "诊断", "异常", "自适应", "diag"]):
            plan.append({"agent": "ai_bios", "action": "diagnose", "params": {}})
        if any(k in g for k in ["主板", "适配", "mainboard", "porting"]):
            plan.append({"agent": "mainboard_adapt", "action": "adapt", "params": {}})
        if not plan:
            plan = [{"agent": "boot_flow", "action": "analyze", "params": {}},
                    {"agent": "firmware_security", "action": "secure_boot", "params": {}},
                    {"agent": "ai_bios", "action": "diagnose", "params": {}}]
        return plan

    def execute(self, goal: str, plan: List[Dict[str, Any]], params: Dict[str, Any]) -> Dict[str, Any]:
        results = []
        for step in plan:
            agent_name = step["agent"]
            agent_cls, _ = AGENT_REGISTRY[agent_name]
            agent = agent_cls(config={}, data_dir=self.data_dir)
            task = dict(step.get("params", {}))
            task.update(params)
            task["action"] = step.get("action", "default")
            try:
                res = agent.run(task)
                results.append({"agent": agent_name, "ok": True, "result": res})
            except Exception as exc:  # noqa: BLE001
                logger.exception("Agent %s 失败", agent_name)
                results.append({"agent": agent_name, "ok": False, "error": str(exc)})
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        report = {"task_id": task_id, "goal": goal, "plan": plan, "results": results,
                  "status": "done", "created_at": int(time.time())}
        self._tasks[task_id] = report
        return report

    def run(self, goal: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        params = params or {}
        plan = self.plan(goal)
        return self.execute(goal, plan, params)

    def get_task(self, task_id: str) -> Dict[str, Any] | None:
        return self._tasks.get(task_id)

    def list_agents(self) -> List[Dict[str, Any]]:
        return [{"name": name, "description": desc, "action_hint": self._hint(name)}
                for name, (cls, desc) in AGENT_REGISTRY.items()]

    def _hint(self, name: str) -> str:
        hints = {"boot_flow": "analyze / post", "firmware_security": "secure_boot / supply_chain",
                 "ai_bios": "diagnose / adaptive", "mainboard_adapt": "adapt"}
        return hints.get(name, "")
