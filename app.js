const STATUS_LABEL = {
  green: "流畅",
  yellow: "拥挤",
  red: "失效",
  unknown: "检测中",
};

let services = [];
let statusMap = {};
let activeCategory = "全部";

async function load() {
  const [servicesRes, statusRes] = await Promise.all([
    fetch("data/services.json"),
    fetch("data/status.json").catch(() => null),
  ]);
  services = await servicesRes.json();

  if (statusRes && statusRes.ok) {
    const statusData = await statusRes.json();
    statusMap = statusData.services || {};
    document.getElementById("updated-at").textContent = new Date(statusData.updated_at).toLocaleString("zh-CN");
  } else {
    document.getElementById("updated-at").textContent = "暂无数据";
  }

  renderFilters();
  render();
}

function renderFilters() {
  const categories = ["全部", ...new Set(services.map((s) => s.category))];
  const container = document.getElementById("filters");
  container.innerHTML = "";
  categories.forEach((cat) => {
    const btn = document.createElement("button");
    btn.className = "filter-btn" + (cat === activeCategory ? " active" : "");
    btn.textContent = cat;
    btn.onclick = () => {
      activeCategory = cat;
      renderFilters();
      render();
    };
    container.appendChild(btn);
  });
}

function render() {
  const keyword = document.getElementById("search").value.trim().toLowerCase();
  const grid = document.getElementById("grid");
  grid.innerHTML = "";

  services
    .filter((s) => activeCategory === "全部" || s.category === activeCategory)
    .filter((s) => !keyword || s.name.toLowerCase().includes(keyword) || s.desc.toLowerCase().includes(keyword))
    .forEach((s) => {
      const status = (statusMap[s.id] && statusMap[s.id].status) || "unknown";
      const card = document.createElement("a");
      card.className = "card";
      card.href = s.url;
      card.target = "_blank";
      card.rel = "noopener noreferrer";
      card.innerHTML = `
        <div class="card-top">
          <span class="card-name">${s.name}</span>
          <span class="dot ${status}" title="${STATUS_LABEL[status]}"></span>
        </div>
        <p class="card-desc">${s.desc}</p>
        <p class="card-status-text">${STATUS_LABEL[status]}</p>
      `;
      grid.appendChild(card);
    });
}

document.getElementById("search").addEventListener("input", render);
load();
