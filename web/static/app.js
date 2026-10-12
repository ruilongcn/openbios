/* 固件（BIOS/AI BIOS）智能体团队 - 前端交互 */
"use strict";

/* ---------- Tab 切换 ---------- */
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('view-' + btn.dataset.view).classList.add('active');
  });
});

async function api(path, body) {
  const opt = { headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) opt.method = 'POST', opt.body = JSON.stringify(body);
  const resp = await fetch(path, opt);
  if (!resp.ok) throw new Error('HTTP ' + resp.status);
  return resp.json();
}
function show(el, data) {
  el.classList.remove('hidden');
  el.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
}

/* 启动流程 */
async function bootAnalyze() {
  const r = await api('/api/tasks', { goal: '分析固件启动流程', params: { action: 'analyze', firmware_type: document.getElementById('bootType').value } });
  show(document.getElementById('bootResult'), r.results[0].result);
}
async function bootPost() {
  const r = await api('/api/tasks', { goal: '生成 POST 自检清单', params: { action: 'post' } });
  show(document.getElementById('bootResult'), r.results[0].result);
}

/* 固件安全 */
async function secBoot() {
  const r = await api('/api/tasks', { goal: '评估固件安全策略', params: { action: 'secure_boot' } });
  show(document.getElementById('secResult'), r.results[0].result);
}
async function secChain() {
  const r = await api('/api/tasks', { goal: '防供应链投毒', params: { action: 'supply_chain' } });
  show(document.getElementById('secResult'), r.results[0].result);
}

/* AI BIOS */
async function aiDiag() {
  const r = await api('/api/tasks', {
    goal: 'AI BIOS 智能诊断',
    params: { action: 'diagnose', symptoms: document.getElementById('diagSymptom').value.split(',').map(s => s.trim()).filter(Boolean) }
  });
  show(document.getElementById('aiResult'), r.results[0].result);
}
async function aiAdaptive() {
  const r = await api('/api/tasks', { goal: 'AI BIOS 自适应配置', params: { action: 'adaptive', workload: 'general' } });
  show(document.getElementById('aiResult'), r.results[0].result);
}

/* 主板适配 */
async function boardAdapt() {
  const r = await api('/api/tasks', { goal: '主板适配规划', params: { action: 'adapt', board_name: document.getElementById('boardName').value } });
  show(document.getElementById('boardResult'), r.results[0].result);
}

/* 流水线 */
async function plRun() {
  const r = await api('/api/tasks', { goal: document.getElementById('plGoal').value || '分析启动流程、评估固件安全并做 AI 诊断', params: {} });
  show(document.getElementById('plResult'), r);
}

/* 系统 */
async function loadSystem() {
  try {
    const h = await api('/api/health');
    document.getElementById('sysHealth').textContent = JSON.stringify(h, null, 2);
    const a = await api('/api/agents');
    document.getElementById('sysCards').innerHTML = a.agents.map(x => `<div class="card"><b>${x.name}</b><div class="hint">${x.description}</div></div>`).join('');
  } catch (e) { document.getElementById('sysHealth').textContent = '错误: ' + e.message; }
}
loadSystem();
