# -*- coding: utf-8 -*-
"""AI BIOS Agent：固件智能诊断、启动异常分析、自适应配置。

能力：
- 启动异常分析（结合日志/事件生成诊断报告）；
- 自适应配置建议（内存/风扇/功耗/启动顺序）；
- 输出 data/aibios/diag_*.json 契约。
"""
from __future__ import annotations

import time
from typing import Any, Dict

from .base_agent import BaseAgent


class AIBIOSAgent(BaseAgent):
    name = "ai_bios"
    description = "AI BIOS：固件智能诊断、启动异常分析、自适应配置建议"

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "diagnose")
        if action == "adaptive":
            return self._adaptive(task)
        return self._diagnose(task)

    def _diagnose(self, task: Dict[str, Any]) -> Dict[str, Any]:
        symptoms = task.get("symptoms", ["开机黑屏", "启动缓慢", "蓝屏"])
        log_lines = task.get("logs", [])
        diagnosis = {
            "symptoms": symptoms,
            "log_analysis": self._analyze_logs(log_lines),
            "root_cause_candidates": [
                {"symptom": "开机黑屏", "causes": ["内存未正确初始化", "显卡驱动/固件失配", "供电异常", "BIOS 设置错误"]},
                {"symptom": "启动缓慢", "causes": ["POST 卡在设备枚举", "存储介质故障", "Fast Boot 未开启"]},
                {"symptom": "蓝屏", "causes": ["内存错误（ECC 告警）", "驱动冲突", "固件与 OS 兼容问题"]},
            ],
            "recommended_actions": [
                "更新固件到稳定版本（签名校验后）",
                "复位 CMOS / 加载默认安全设置",
                "逐项测试内存 DIMM（MemTest）",
                "检查 Secure Boot 状态与 db 签名",
            ],
            "ai_note": "启用 LLM 网关后，本 Agent 可结合日志自动生成更细粒度根因分析与修复步骤",
            "generated_at": int(time.time()),
        }
        path = self._write_contract("aibios", f"diag_{int(time.time())}.json", diagnosis)
        diagnosis["contract_path"] = str(path)
        return {"status": "ok", **diagnosis}

    def _analyze_logs(self, log_lines) -> str:
        if not log_lines:
            return "未提供日志，基于症状库规则诊断"
        hits = []
        for line in log_lines:
            low = line.lower()
            if "memory" in low or "内存" in line:
                hits.append("检测到内存相关事件")
            if "secure boot" in low or "签名" in line:
                hits.append("检测到安全启动相关事件")
            if "disk" in low or "存储" in line:
                hits.append("检测到存储相关事件")
        return "；".join(hits) if hits else "日志未命中已知模式，建议启用 LLM 深度分析"

    def _adaptive(self, task: Dict[str, Any]) -> Dict[str, Any]:
        workload = task.get("workload", "general")
        profiles = {
            "general": {"power_profile": "平衡", "fan_curve": "标准", "boot": "正常"},
            "gaming": {"power_profile": "高性能", "fan_curve": "激进", "boot": "快速"},
            "server": {"power_profile": "节能", "fan_curve": "静音", "boot": "严格校验"},
            "low_power": {"power_profile": "省电", "fan_curve": "静音", "boot": "快速"},
        }
        cfg = profiles.get(workload, profiles["general"])
        payload = {
            "workload": workload,
            "adaptive_config": cfg,
            "auto_tuning": [
                "根据负载动态调整 CPU 睿频/功耗墙",
                "根据温度调整风扇曲线",
                "按使用习惯自动调整启动顺序",
                "XMP/内存时序自动优化（可选）",
            ],
            "user_control": "所有自适应策略均提供手动覆盖开关，尊重用户最终选择",
            "generated_at": int(time.time()),
        }
        path = self._write_contract("aibios", f"adaptive_{int(time.time())}.json", payload)
        payload["contract_path"] = str(path)
        return {"status": "ok", **payload}
