# AI 工具导航

只收录官方渠道的免费额度 AI 产品，实时监测可用状态（🟢流畅 / 🟡拥挤 / 🔴失效），
不收录任何第三方中转/镜像站。

## 目录结构

```
ai-nav/
├── index.html          页面结构
├── style.css            样式（含暗色模式）
├── app.js                前端渲染逻辑
├── monitor.py            探活脚本，生成 data/status.json
├── data/
│   ├── services.json     产品清单（手动维护）
│   └── status.json       探活结果（自动生成，不要手动改）
├── images/                放二维码等图片
└── .github/workflows/monitor.yml   每 30 分钟自动探活并提交
```

## 本地预览

```bash
python -m http.server 8000
# 浏览器打开 http://localhost:8000
```

## 探活脚本

```bash
python monitor.py
```

会读取 `data/services.json`，逐个请求，把结果写到 `data/status.json`。
判定逻辑：
- 🟢 green：200 且 3 秒内响应
- 🟡 yellow：200 但响应慢（3~8秒），或被反爬拦截（401/403/429，无法判断真实状态时保守显示"拥挤"而非直接判死，避免误伤）
- 🔴 red：请求失败 / 超时 / 明确的服务端错误

## 部署到 GitHub Pages + 免费自动探活

1. 新建 GitHub 仓库，push 这个目录
2. 仓库 Settings → Pages → 选 `main` 分支根目录部署
3. `.github/workflows/monitor.yml` 已经配置好，每 30 分钟自动跑一次 `monitor.py` 并提交 `status.json`，全程零成本（GitHub Actions 免费额度足够）
4. 如果想改探活频率，改 workflow 里的 cron 表达式

## 免责声明文案（放在 footer，可直接用）

> 本站仅收录各产品官方地址，不提供任何第三方中转/镜像服务。可用性数据仅供参考，
> 具体免费额度、使用政策请以各官方产品最新公告为准。
