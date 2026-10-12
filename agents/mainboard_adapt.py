# -*- coding: utf-8 -*-
"""主板适配 Agent：固件到具体主板的适配规划。

能力：
- 生成主板适配清单（芯片组、SuperIO、EC、时钟、GPIO、传感器）；
- 输出 data/mainboard/adapt_*.json 契约。
"""
from __future__ import annotations

import time
from typing import Any, Dict

from .base_agent import BaseAgent


class MainboardAdaptAgent(BaseAgent):
    name = "mainboard_adapt"
    description = "主板适配：芯片组/SuperIO/EC/GPIO/传感器适配清单与验证计划"

    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "adapt")
        return self._adapt(task)

    def _adapt(self, task: Dict[str, Any]) -> Dict[str, Any]:
        board = task.get("board_name", "CN-ATX-B760")
        chipset = task.get("chipset", "自主芯片组 CN-PCH")
        payload = {
            "board_name": board,
            "chipset": chipset,
            "adaptation_items": [
                {"module": "芯片组初始化", "detail": "内存控制器、PCIe Root Complex、电源管理"},
                {"module": "SuperIO", "detail": "EC/传感器：温控、风扇、电压监控（SMBus 挂载）"},
                {"module": "嵌入式控制器 EC", "detail": "键盘、电池、功耗策略（笔记本场景）"},
                {"module": "时钟发生器", "detail": "PLL/Clockgen 配置"},
                {"module": "GPIO 映射", "detail": "上电时序、复位信号、LED/按键"},
                {"module": "传感器 HWM", "detail": "NTC 温度、风扇转速、电压采集"},
            ],
            "porting_steps": [
                "获取主板原理图与芯片组 datasheet",
                "建立 ACPI 表（DSDT/SSDT）与设备树",
                "配置内存初始化参数（SPD/时序）",
                "驱动移植：EC/网卡/声卡/USB 控制器",
                "验证上电时序与各电源轨",
            ],
            "verification": ["POST 通过", "ACPI 休眠/唤醒", "温度/风扇闭环", "长时间稳定性测试"],
            "generated_at": int(time.time()),
        }
        path = self._write_contract("mainboard", f"adapt_{int(time.time())}.json", payload)
        payload["contract_path"] = str(path)
        return {"status": "ok", **payload}
