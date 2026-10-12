---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: d32db8dd5a6f99a1df3565db906abe3a_c3888628c07211f197eb525400393706
    ReservedCode1: eibvXxrSLwFNL+LT0bWoN81qIeP8xWwUfi8WHHBQg0iQAvyfdMo+d0gA0etlKT2fFztoI0kleb9rK7h7E7R1A9y580qm7czAw9FPxbufflzaP7A1/pq7WnOVMS+olyfyYMuCVPRSjLHy7lx3ljyB/qf2u5kvmvVnfDv4GPrSOLjQa2+G4ZaRQ0U2aKQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: d32db8dd5a6f99a1df3565db906abe3a_c3888628c07211f197eb525400393706
    ReservedCode2: eibvXxrSLwFNL+LT0bWoN81qIeP8xWwUfi8WHHBQg0iQAvyfdMo+d0gA0etlKT2fFztoI0kleb9rK7h7E7R1A9y580qm7czAw9FPxbufflzaP7A1/pq7WnOVMS+olyfyYMuCVPRSjLHy7lx3ljyB/qf2u5kvmvVnfDv4GPrSOLjQa2+G4ZaRQ0U2aKQ=
---

# 固件（BIOS/AI BIOS）智能体团队（Firmware Agent Team）

面向自主可控固件（BIOS/UEFI/OpenFirmware + AI BIOS）研发的网页版专业智能体团队软件。覆盖固件启动流程、固件安全、AI BIOS 与主板适配。

## 技术栈

- **后端**：FastAPI + Uvicorn（Python 3.11+）
- **多智能体流水线**：Orchestrator 意图解析 → 路由 Agent → JSON 契约落盘（data/）
- **前端**：原生 HTML + CSS + JavaScript（零构建、零依赖）
- **LLM 网关**：云端优先，失败自动降级本地 Ollama（纯规则引擎不依赖 LLM 也可运行）

## 智能体团队

| Agent | 职责 |
|---|---|
| boot_flow | 固件启动流程：POST 上电自检、UEFI 四阶段、OpenFirmware 对照、启动卡点诊断 |
| firmware_security | 固件安全：Secure Boot、固件签名链、防供应链投毒、密钥管理 |
| ai_bios | AI BIOS：固件智能诊断、启动异常分析、自适应配置 |
| mainboard_adapt | 主板适配：芯片组/SuperIO/EC/GPIO/传感器适配 |

## 快速启动

### 方式一：双击脚本（Windows）

```bat
scripts\start.bat
```

### 方式二：命令行

```powershell
cd F:\openbios
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scripts\start_backend.py
```

启动后浏览器访问：<http://127.0.0.1:8002>

## 目录结构

```
F:\openbios\
├── agents\            # 多智能体（boot_flow / firmware_security / ai_bios / mainboard_adapt）
├── services\          # llm_gateway
├── web\               # FastAPI 入口 + static 前端
├── scripts\           # 启动脚本
├── config\            # models.json + .env.example
├── data\              # Agent 产出契约（bootflow/security/aibios/mainboard）
├── requirements.txt
├── README.md
└── 技术方案.md
```

## API 一览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | / | 前端页面 |
| GET | /api/health | 健康检查 + LLM 状态 |
| GET | /api/agents | Agent 列表 |
| POST | /api/tasks | 提交目标，Orchestrator 规划并执行 |
| GET | /api/tasks/{id} | 查询任务报告 |
| GET | /api/contracts/{sub_dir} | 浏览 data/ 下契约产物 |

详细设计见 [技术方案.md](技术方案.md)。
*（内容由AI生成，仅供参考）*
