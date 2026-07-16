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

## 待办（上线前必须做）

- [ ] 把你自己的公众号二维码放到 `images/wechat-qr.png`
- [ ] 把你自己的 QQ 群二维码放到 `images/qq-qr.png`
- [ ] 确认 `data/services.json` 里每个 URL 都是当前有效的官方地址（这类产品改域名/改免费政策比较频繁，建议每月人工复查一次）
- [ ] 换一个跟"房产"业务完全无关的域名/子域名

## 关键词策略（供页面 title/description、内容更新参考）

选品和内容围绕这些方向的搜索需求展开，全部对应真实存在的官方免费额度，不涉及未授权中转：

| 关键词方向 | 示例词 |
|---|---|
| 国际大模型免费额度 | "Gemini 免费额度"、"Gemini API 免费申请"、"Groq 免费API怎么用" |
| 国产大模型免费使用 | "DeepSeek 免费使用"、"Kimi 长文本免费"、"豆包 免费版"、"通义千问 免费额度" |
| 开源模型免费部署/体验 | "HuggingFace Spaces 免费部署"、"开源大模型在线体验" |
| 教程/对比类长尾词 | "国产AI大模型免费额度对比"、"2026 免费AI工具推荐"、"AI 写作 免费工具" |

这类词流量不如"ChatGPT镜像""免翻墙"那么大，但转化的用户更稳定、账号/公众号被封的风险也低很多，适合长期做。

## 免责声明文案（放在 footer，可直接用）

> 本站仅收录各产品官方地址，不提供任何第三方中转/镜像服务。可用性数据仅供参考，
> 具体免费额度、使用政策请以各官方产品最新公告为准。
