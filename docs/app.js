const docs = window.CHANGFA_DOCS || [];
const visualAssets = window.CHANGFA_VISUAL_ASSETS || [];
const REPO_EDIT_BASE = "https://github.com/a295415099-ux/changfa-xiaozhai-ai/edit/main/";
const APP_STORAGE_VERSION = "20260707-dashboard-redesign";
const GROUP_ORDER = [
  "总控导航",
  "AI项目执行",
  "电商资料库",
  "资料库说明",
  "模板库",
  "架构与总控",
  "竞品分析",
  "Jessie Skill库",
];
const VISUAL_TYPE_META = {
  hero: {
    title: "首图",
    description: "按产品、平台和版本查看主图、搜索首图、货架图及点击数据。",
  },
  detail: {
    title: "商详页",
    description: "阅读完整商详长图，对照卖点结构、承接表现和转化数据。",
  },
  home: {
    title: "平台首页",
    description: "集中查看天猫、淘宝、京东、抖音等平台首页及版本变化。",
  },
};

const state = {
  currentId: docs[0]?.id || null,
  mode: "view",
  query: "",
  activeGroup: "全部",
  lightboxMode: "fit",
  surface: "document",
  visualType: "hero",
  visualProduct: "全部产品",
  visualPlatform: "全部平台",
  visualStatus: "全部状态",
  visualCollectionId: null,
  visualMediaIndex: 0,
};

const els = {
  sidebar: document.getElementById("sidebar"),
  sidebarBackdrop: document.getElementById("sidebarBackdrop"),
  mobileMenuButton: document.getElementById("mobileMenuButton"),
  sidebarCloseButton: document.getElementById("sidebarCloseButton"),
  mobileDocGroup: document.getElementById("mobileDocGroup"),
  commandPanel: document.getElementById("commandPanel"),
  mobileSearchPanel: document.getElementById("mobileSearchPanel"),
  statusStrip: document.getElementById("statusStrip"),
  totalDocs: document.getElementById("totalDocs"),
  totalGroups: document.getElementById("totalGroups"),
  resultCount: document.getElementById("resultCount"),
  groupFilters: document.getElementById("groupFilters"),
  mobileGroupFilters: document.getElementById("mobileGroupFilters"),
  docList: document.getElementById("docList"),
  docGroup: document.getElementById("docGroup"),
  pageNumber: document.getElementById("pageNumber"),
  docTitle: document.getElementById("docTitle"),
  docPath: document.getElementById("docPath"),
  reader: document.getElementById("reader"),
  editorPanel: document.getElementById("editorPanel"),
  editor: document.getElementById("editor"),
  searchInput: document.getElementById("searchInput"),
  mobileSearchInput: document.getElementById("mobileSearchInput"),
  viewButton: document.getElementById("viewButton"),
  editButton: document.getElementById("editButton"),
  copyButton: document.getElementById("copyButton"),
  downloadButton: document.getElementById("downloadButton"),
  githubEditButton: document.getElementById("githubEditButton"),
  resetButton: document.getElementById("resetButton"),
  saveButton: document.getElementById("saveButton"),
  saveStatus: document.getElementById("saveStatus"),
  editorHint: document.getElementById("editorHint"),
  visualWorkspace: document.getElementById("visualWorkspace"),
  visualWorkspaceTitle: document.getElementById("visualWorkspaceTitle"),
  visualWorkspaceDescription: document.getElementById("visualWorkspaceDescription"),
  visualResultCount: document.getElementById("visualResultCount"),
  visualFilteredCount: document.getElementById("visualFilteredCount"),
  visualProductFilter: document.getElementById("visualProductFilter"),
  visualPlatformFilter: document.getElementById("visualPlatformFilter"),
  visualStatusFilter: document.getElementById("visualStatusFilter"),
  visualEmptyState: document.getElementById("visualEmptyState"),
  visualLayout: document.getElementById("visualLayout"),
  visualCollectionList: document.getElementById("visualCollectionList"),
  visualViewer: document.getElementById("visualViewer"),
};

const groups = [
  "全部",
  ...Array.from(new Set(docs.map((doc) => doc.group))).sort((a, b) => {
    const indexA = GROUP_ORDER.indexOf(a);
    const indexB = GROUP_ORDER.indexOf(b);
    if (indexA !== -1 || indexB !== -1) {
      return (indexA === -1 ? 999 : indexA) - (indexB === -1 ? 999 : indexB);
    }
    return a.localeCompare(b, "zh-CN");
  }),
];

const lightbox = document.createElement("div");
lightbox.className = "lightbox";
lightbox.hidden = true;
lightbox.innerHTML = `
  <div class="lightbox-toolbar">
    <div class="lightbox-title" id="lightboxTitle"></div>
    <div class="lightbox-actions">
      <button type="button" id="lightboxModeButton">按宽度查看</button>
      <a id="lightboxOpenButton" href="#" target="_blank" rel="noreferrer">原图</a>
      <button type="button" id="lightboxCloseButton">关闭</button>
    </div>
  </div>
  <div class="lightbox-stage" id="lightboxStage">
    <img id="lightboxImage" alt="">
  </div>
`;
document.body.appendChild(lightbox);

const lightboxEls = {
  title: document.getElementById("lightboxTitle"),
  image: document.getElementById("lightboxImage"),
  stage: document.getElementById("lightboxStage"),
  modeButton: document.getElementById("lightboxModeButton"),
  openButton: document.getElementById("lightboxOpenButton"),
  closeButton: document.getElementById("lightboxCloseButton"),
};

function storageKey(id) {
  return `changfa-doc:${APP_STORAGE_VERSION}:${id}`;
}

function getDoc(id) {
  return docs.find((doc) => doc.id === id) || docs[0];
}

function getContent(doc) {
  return localStorage.getItem(storageKey(doc.id)) || doc.markdown;
}

function setStatus(message) {
  els.saveStatus.textContent = message;
  els.editorHint.textContent = message;
}

function setContent(doc, value) {
  localStorage.setItem(storageKey(doc.id), value);
  setStatus("已保存到当前浏览器");
}

function resetContent(doc) {
  localStorage.removeItem(storageKey(doc.id));
  setStatus("已恢复原文");
}

function displayText(value) {
  return String(value).replace(/[\u2014\u2013]/g, "-");
}

function escapeHtml(value) {
  return displayText(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function inlineMarkdown(value) {
  return escapeHtml(value)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
}

function parseTable(lines, startIndex) {
  const rows = [];
  let index = startIndex;
  while (index < lines.length && /^\|.*\|$/.test(lines[index].trim())) {
    rows.push(lines[index].trim());
    index += 1;
  }
  if (rows.length < 2 || !/^\|[\s:-|]+\|$/.test(rows[1])) return null;
  const htmlRows = rows
    .filter((_, rowIndex) => rowIndex !== 1)
    .map((row, rowIndex) => {
      const cells = row.slice(1, -1).split("|").map((cell) => cell.trim());
      const tag = rowIndex === 0 ? "th" : "td";
      return `<tr>${cells.map((cell) => `<${tag}>${inlineMarkdown(cell)}</${tag}>`).join("")}</tr>`;
    })
    .join("");
  return { html: `<div class="table-wrap"><table>${htmlRows}</table></div>`, nextIndex: index };
}

function markdownToHtml(markdown) {
  const lines = markdown.split(/\r?\n/);
  const html = [];
  let index = 0;
  let inCode = false;
  let code = [];
  let list = [];

  function flushList() {
    if (!list.length) return;
    html.push(`<ul>${list.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("")}</ul>`);
    list = [];
  }

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();

    if (trimmed.startsWith("```")) {
      if (inCode) {
        html.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
        code = [];
        inCode = false;
      } else {
        flushList();
        inCode = true;
      }
      index += 1;
      continue;
    }

    if (inCode) {
      code.push(line);
      index += 1;
      continue;
    }

    if (!trimmed) {
      flushList();
      index += 1;
      continue;
    }

    const table = parseTable(lines, index);
    if (table) {
      flushList();
      html.push(table.html);
      index = table.nextIndex;
      continue;
    }

    if (trimmed.startsWith(">")) {
      flushList();
      html.push(`<blockquote>${inlineMarkdown(trimmed.replace(/^>\s?/, ""))}</blockquote>`);
      index += 1;
      continue;
    }

    const image = trimmed.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
    if (image) {
      flushList();
      html.push(`
        <figure class="asset-figure">
          <button class="asset-preview" type="button" data-image-src="${escapeHtml(image[2])}" data-image-title="${escapeHtml(image[1])}" aria-label="全屏查看 ${escapeHtml(image[1])}">
            <img src="${escapeHtml(image[2])}" alt="${escapeHtml(image[1])}" loading="lazy">
          </button>
          <figcaption>${escapeHtml(image[1])}</figcaption>
        </figure>
      `);
      index += 1;
      continue;
    }

    const heading = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      flushList();
      const level = Math.min(heading[1].length, 3);
      html.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      index += 1;
      continue;
    }

    const bullet = trimmed.match(/^[-*]\s+(.+)$/);
    if (bullet) {
      list.push(bullet[1]);
      index += 1;
      continue;
    }

    const ordered = trimmed.match(/^\d+\.\s+(.+)$/);
    if (ordered) {
      list.push(ordered[1]);
      index += 1;
      continue;
    }

    flushList();
    html.push(`<p>${inlineMarkdown(trimmed)}</p>`);
    index += 1;
  }

  flushList();
  if (inCode) html.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
  return html.join("\n");
}

function docSummary(doc) {
  const text = doc.markdown
    .replace(/^#.+$/m, "")
    .replace(/[`#>*|\-[\]()]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return text.slice(0, 78);
}

function getFilteredDocs() {
  const query = state.query.trim().toLowerCase();
  return docs.filter((doc) => {
    const groupMatch = state.activeGroup === "全部" || doc.group === state.activeGroup;
    if (!groupMatch) return false;
    if (!query) return true;
    return `${doc.title} ${doc.group} ${doc.path} ${doc.markdown}`.toLowerCase().includes(query);
  });
}

function groupDocs(filteredDocs) {
  return filteredDocs.reduce((result, doc) => {
    if (!result[doc.group]) result[doc.group] = [];
    result[doc.group].push(doc);
    return result;
  }, {});
}

function renderStats(filteredDocs) {
  els.totalDocs.textContent = docs.length;
  els.totalGroups.textContent = groups.length - 1;
  els.resultCount.textContent = filteredDocs.length;
}

function renderGroupFilters(filteredDocs) {
  const counts = docs.reduce((result, doc) => {
    result[doc.group] = (result[doc.group] || 0) + 1;
    return result;
  }, {});
  const buttons = groups.map((group) => {
    const active = state.activeGroup === group ? " active" : "";
    const count = group === "全部" ? docs.length : counts[group] || 0;
    return `<button class="filter-chip${active}" type="button" data-group="${escapeHtml(group)}">${escapeHtml(group)}<span>${count}</span></button>`;
  }).join("");
  els.groupFilters.innerHTML = buttons;
  els.mobileGroupFilters.innerHTML = buttons;
  els.resultCount.textContent = filteredDocs.length;
}

function renderNav() {
  const filtered = getFilteredDocs();
  const grouped = groupDocs(filtered);
  renderStats(filtered);
  renderGroupFilters(filtered);

  if (!filtered.length) {
    els.docList.innerHTML = `
      <div class="empty-state">
        <strong>没有匹配结果</strong>
        <span>换一个关键词，或切回“全部”。</span>
      </div>
    `;
    return;
  }

  els.docList.innerHTML = Object.entries(grouped)
    .sort(([groupA], [groupB]) => groups.indexOf(groupA) - groups.indexOf(groupB))
    .map(([group, groupDocs]) => {
      const cards = groupDocs.map((doc) => {
        const selected = doc.id === state.currentId ? " selected" : "";
        return `
          <button class="doc-card${selected}" type="button" data-id="${doc.id}">
            <span class="doc-card-number">${escapeHtml(doc.number || "--")}</span>
            <span class="doc-card-title">${escapeHtml(doc.title)}</span>
            <span class="doc-card-summary">${escapeHtml(docSummary(doc))}</span>
            <span class="doc-card-path">${escapeHtml(doc.path)}</span>
          </button>
        `;
      }).join("");
      return `<section class="doc-group"><h3>${escapeHtml(group)}<span>${groupDocs.length}</span></h3>${cards}</section>`;
    })
    .join("");
}

function setVisualOptions(select, allLabel, values, currentValue) {
  const options = [allLabel, ...Array.from(new Set(values.filter(Boolean))).sort((a, b) => a.localeCompare(b, "zh-CN"))];
  const selected = options.includes(currentValue) ? currentValue : allLabel;
  select.innerHTML = options
    .map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`)
    .join("");
  select.value = selected;
  return selected;
}

function getVisualCollectionsByType() {
  return visualAssets
    .filter((collection) => collection.type === state.visualType)
    .sort((a, b) => `${b.date || ""} ${b.version || ""}`.localeCompare(`${a.date || ""} ${a.version || ""}`, "zh-CN"));
}

function getFilteredVisualCollections() {
  return getVisualCollectionsByType().filter((collection) => {
    const productMatch = state.visualProduct === "全部产品" || collection.product === state.visualProduct;
    const platformMatch = state.visualPlatform === "全部平台" || collection.platform === state.visualPlatform;
    const statusMatch = state.visualStatus === "全部状态" || collection.status === state.visualStatus;
    return productMatch && platformMatch && statusMatch;
  });
}

function visualMediaPreview(media, title) {
  if (!media) return '<span class="visual-preview-placeholder">待上传</span>';
  if (media.kind === "video") {
    return `<span class="visual-preview-placeholder">视频</span>`;
  }
  return `<img src="${escapeHtml(media.src)}" alt="${escapeHtml(title)}" loading="lazy">`;
}

function renderVisualCollectionList(collections) {
  els.visualCollectionList.innerHTML = collections.map((collection) => {
    const selected = collection.id === state.visualCollectionId ? " selected" : "";
    const firstMedia = collection.media?.[0];
    return `
      <button class="visual-collection-card${selected}" type="button" data-visual-collection-id="${escapeHtml(collection.id)}">
        <span class="visual-collection-preview">${visualMediaPreview(firstMedia, collection.version)}</span>
        <span class="visual-collection-copy">
          <strong>${escapeHtml(collection.product)}</strong>
          <span>${escapeHtml(collection.platform)} / ${escapeHtml(collection.version)}</span>
          <small>${escapeHtml(collection.date || "日期待补")} / ${escapeHtml(collection.status || "待整理")}</small>
        </span>
      </button>
    `;
  }).join("");
}

function metricValue(metric, chineseKey, englishKey) {
  return metric?.[chineseKey] ?? metric?.[englishKey] ?? "";
}

function renderVisualMetrics(metrics) {
  if (!metrics?.length) {
    return `
      <div class="visual-data-empty">
        <strong>暂未录入数据</strong>
        <span>在版本文件夹加入 _数据.csv 后，会在这里显示上线前后对比。</span>
      </div>
    `;
  }
  const rows = metrics.map((metric) => `
    <tr>
      <th>${escapeHtml(metricValue(metric, "指标", "label") || "待定义")}</th>
      <td>${escapeHtml(metricValue(metric, "上线前", "before") || "待补")}</td>
      <td>${escapeHtml(metricValue(metric, "上线后", "after") || "待补")}</td>
      <td>${escapeHtml(metricValue(metric, "变化", "change") || "待复盘")}</td>
      <td>${escapeHtml(metricValue(metric, "结论", "conclusion") || "")}</td>
    </tr>
  `).join("");
  return `
    <div class="visual-data-table-wrap">
      <table class="visual-data-table">
        <thead><tr><th>指标</th><th>上线前</th><th>上线后</th><th>变化</th><th>结论</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function renderVisualViewer(collection) {
  if (!collection) {
    els.visualViewer.innerHTML = "";
    return;
  }
  const media = collection.media || [];
  const safeIndex = Math.min(state.visualMediaIndex, Math.max(media.length - 1, 0));
  state.visualMediaIndex = safeIndex;
  const activeMedia = media[safeIndex];
  const stage = activeMedia?.kind === "video"
    ? `<video src="${escapeHtml(activeMedia.src)}" controls preload="metadata"></video>`
    : activeMedia
      ? `<button class="visual-stage-open" type="button" data-visual-image-src="${escapeHtml(activeMedia.src)}" data-visual-image-title="${escapeHtml(activeMedia.title || collection.version)}" aria-label="全屏查看 ${escapeHtml(activeMedia.title || collection.version)}"><img src="${escapeHtml(activeMedia.src)}" alt="${escapeHtml(activeMedia.title || collection.version)}"></button>`
      : '<div class="visual-stage-missing">这个版本还没有上传画面</div>';
  const mediaStrip = media.length > 1
    ? `<div class="visual-media-strip">${media.map((item, index) => `
        <button class="visual-media-thumb${index === safeIndex ? " active" : ""}" type="button" data-visual-media-index="${index}" aria-label="查看第 ${index + 1} 张">
          ${visualMediaPreview(item, item.title || `${collection.version} ${index + 1}`)}
          <span>${String(index + 1).padStart(2, "0")}</span>
        </button>
      `).join("")}</div>`
    : "";

  els.visualViewer.innerHTML = `
    <header class="visual-viewer-header">
      <div>
        <p>${escapeHtml(collection.project || "待关联项目")}</p>
        <h3>${escapeHtml(collection.product)} / ${escapeHtml(collection.version)}</h3>
      </div>
      <dl class="visual-meta-list">
        <div><dt>平台</dt><dd>${escapeHtml(collection.platform || "待补")}</dd></div>
        <div><dt>日期</dt><dd>${escapeHtml(collection.date || "待补")}</dd></div>
        <div><dt>状态</dt><dd>${escapeHtml(collection.status || "待整理")}</dd></div>
        <div><dt>画面</dt><dd>${media.length}</dd></div>
      </dl>
      ${collection.note ? `<p class="visual-note">${escapeHtml(collection.note)}</p>` : ""}
    </header>
    ${mediaStrip}
    <div class="visual-stage">${stage}</div>
    <section class="visual-data-section">
      <div class="visual-data-heading">
        <h4>版本数据</h4>
        <p>用同口径的上线前后数据判断下一版保留什么、修改什么。</p>
      </div>
      ${renderVisualMetrics(collection.metrics)}
    </section>
  `;
}

function updateSurfaceButtons() {
  document.querySelectorAll("[data-visual-type]").forEach((button) => {
    button.classList.toggle("active", state.surface === "visual" && button.dataset.visualType === state.visualType);
  });
}

function renderVisualWorkspace() {
  const meta = VISUAL_TYPE_META[state.visualType];
  const allCollections = getVisualCollectionsByType();
  state.visualProduct = setVisualOptions(
    els.visualProductFilter,
    "全部产品",
    allCollections.map((collection) => collection.product),
    state.visualProduct,
  );
  state.visualPlatform = setVisualOptions(
    els.visualPlatformFilter,
    "全部平台",
    allCollections.map((collection) => collection.platform),
    state.visualPlatform,
  );
  state.visualStatus = setVisualOptions(
    els.visualStatusFilter,
    "全部状态",
    allCollections.map((collection) => collection.status),
    state.visualStatus,
  );

  const collections = getFilteredVisualCollections();
  if (!collections.some((collection) => collection.id === state.visualCollectionId)) {
    state.visualCollectionId = collections[0]?.id || null;
    state.visualMediaIndex = 0;
  }
  const selected = collections.find((collection) => collection.id === state.visualCollectionId);

  els.visualWorkspace.dataset.type = state.visualType;
  els.visualWorkspaceTitle.textContent = meta.title;
  els.visualWorkspaceDescription.textContent = meta.description;
  els.visualResultCount.textContent = allCollections.length;
  els.visualFilteredCount.textContent = collections.length;
  els.visualEmptyState.hidden = collections.length > 0;
  els.visualLayout.hidden = collections.length === 0;
  renderVisualCollectionList(collections);
  renderVisualViewer(selected);
  updateSurfaceButtons();
}

function showVisualWorkspace(type) {
  if (!VISUAL_TYPE_META[type]) return;
  state.surface = "visual";
  state.visualType = type;
  state.visualProduct = "全部产品";
  state.visualPlatform = "全部平台";
  state.visualStatus = "全部状态";
  state.visualCollectionId = null;
  state.visualMediaIndex = 0;
  document.body.classList.add("visual-mode");
  els.commandPanel.hidden = true;
  els.mobileSearchPanel.hidden = true;
  els.statusStrip.hidden = true;
  els.reader.hidden = true;
  els.editorPanel.hidden = true;
  els.visualWorkspace.hidden = false;
  els.mobileDocGroup.textContent = VISUAL_TYPE_META[type].title;
  renderVisualWorkspace();
  els.visualWorkspace.scrollTo({ top: 0, behavior: "smooth" });
}

function renderDocument() {
  const doc = getDoc(state.currentId);
  if (!doc) return;
  state.surface = "document";
  document.body.classList.remove("visual-mode");
  els.visualWorkspace.hidden = true;
  els.commandPanel.hidden = false;
  els.mobileSearchPanel.hidden = false;
  els.statusStrip.hidden = false;
  const content = getContent(doc);
  state.currentId = doc.id;
  els.docGroup.textContent = displayText(doc.group);
  els.mobileDocGroup.textContent = displayText(doc.group);
  els.pageNumber.textContent = displayText(doc.number || "--");
  els.docTitle.textContent = displayText(doc.title);
  els.docPath.textContent = displayText(doc.path);
  els.reader.innerHTML = markdownToHtml(content);
  els.editor.value = content;
  els.reader.hidden = state.mode !== "view";
  els.editorPanel.hidden = state.mode !== "edit";
  els.viewButton.classList.toggle("active", state.mode === "view");
  els.editButton.classList.toggle("active", state.mode === "edit");
  updateSurfaceButtons();
  renderNav();
}

function setMode(mode) {
  state.mode = mode;
  renderDocument();
}

function setGroup(group) {
  if (!groups.includes(group)) return;
  state.activeGroup = group;
  state.query = "";
  els.searchInput.value = "";
  els.mobileSearchInput.value = "";
  const filtered = getFilteredDocs();
  if (filtered.length && !filtered.some((doc) => doc.id === state.currentId)) {
    state.currentId = filtered[0].id;
    setStatus("已切换到当前栏目第一篇");
  }
  renderDocument();
}

function setQuery(value) {
  state.query = value;
  if (value.trim()) state.activeGroup = "全部";
  els.searchInput.value = value;
  els.mobileSearchInput.value = value;
  const filtered = getFilteredDocs();
  if (filtered.length && !filtered.some((doc) => doc.id === state.currentId)) {
    state.currentId = filtered[0].id;
  }
  renderDocument();
}

function openSidebar() {
  els.sidebar.classList.add("open");
  els.sidebarBackdrop.hidden = false;
  document.body.classList.add("nav-open");
}

function closeSidebar() {
  els.sidebar.classList.remove("open");
  els.sidebarBackdrop.hidden = true;
  document.body.classList.remove("nav-open");
}

function downloadCurrent() {
  const doc = getDoc(state.currentId);
  const blob = new Blob([getContent(doc)], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${displayText(doc.title).replace(/[\\/:*?"<>|]/g, "-")}.md`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function copyCurrent() {
  const doc = getDoc(state.currentId);
  const content = getContent(doc);
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(content);
  } else {
    const temp = document.createElement("textarea");
    temp.value = content;
    document.body.appendChild(temp);
    temp.select();
    document.execCommand("copy");
    temp.remove();
  }
  setStatus("已复制当前 Markdown");
}

function setLightboxMode(mode) {
  state.lightboxMode = mode;
  lightbox.classList.toggle("fit-width", mode === "width");
  lightboxEls.modeButton.textContent = mode === "fit" ? "按宽度查看" : "适应屏幕";
  lightboxEls.stage.scrollTo({ top: 0, left: 0 });
}

function openLightbox(src, title) {
  lightboxEls.image.src = src;
  lightboxEls.image.alt = title;
  lightboxEls.title.textContent = title || "图片预览";
  lightboxEls.openButton.href = src;
  lightbox.hidden = false;
  document.body.classList.add("lightbox-open");
  setLightboxMode("fit");
  lightboxEls.closeButton.focus();
}

function closeLightbox() {
  lightbox.hidden = true;
  lightboxEls.image.removeAttribute("src");
  document.body.classList.remove("lightbox-open");
}

function handleFilterClick(event) {
  const button = event.target.closest("[data-group]");
  if (!button) return;
  setGroup(button.dataset.group);
}

function handleRouteClick(event) {
  const button = event.target.closest("[data-route-group], [data-route-query], [data-visual-type]");
  if (!button) return;
  if (button.dataset.visualType) {
    showVisualWorkspace(button.dataset.visualType);
  }
  if (button.dataset.routeGroup) {
    setGroup(button.dataset.routeGroup);
  }
  if (button.dataset.routeQuery) {
    setQuery(button.dataset.routeQuery);
  }
  closeSidebar();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

els.docList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-id]");
  if (!button) return;
  state.currentId = button.dataset.id;
  setStatus("网页内编辑会保存到当前浏览器");
  renderDocument();
  closeSidebar();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

els.groupFilters.addEventListener("click", handleFilterClick);
els.mobileGroupFilters.addEventListener("click", handleFilterClick);
els.searchInput.addEventListener("input", (event) => setQuery(event.target.value));
els.mobileSearchInput.addEventListener("input", (event) => setQuery(event.target.value));
els.mobileMenuButton.addEventListener("click", openSidebar);
els.sidebarCloseButton.addEventListener("click", closeSidebar);
els.sidebarBackdrop.addEventListener("click", closeSidebar);
document.addEventListener("click", handleRouteClick);

els.visualProductFilter.addEventListener("change", (event) => {
  state.visualProduct = event.target.value;
  state.visualCollectionId = null;
  state.visualMediaIndex = 0;
  renderVisualWorkspace();
});
els.visualPlatformFilter.addEventListener("change", (event) => {
  state.visualPlatform = event.target.value;
  state.visualCollectionId = null;
  state.visualMediaIndex = 0;
  renderVisualWorkspace();
});
els.visualStatusFilter.addEventListener("change", (event) => {
  state.visualStatus = event.target.value;
  state.visualCollectionId = null;
  state.visualMediaIndex = 0;
  renderVisualWorkspace();
});
els.visualCollectionList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-visual-collection-id]");
  if (!button) return;
  state.visualCollectionId = button.dataset.visualCollectionId;
  state.visualMediaIndex = 0;
  renderVisualWorkspace();
});
els.visualViewer.addEventListener("click", (event) => {
  const mediaButton = event.target.closest("[data-visual-media-index]");
  if (mediaButton) {
    state.visualMediaIndex = Number(mediaButton.dataset.visualMediaIndex) || 0;
    renderVisualWorkspace();
    return;
  }
  const imageButton = event.target.closest("[data-visual-image-src]");
  if (imageButton) {
    openLightbox(imageButton.dataset.visualImageSrc, imageButton.dataset.visualImageTitle);
  }
});

els.reader.addEventListener("click", (event) => {
  const preview = event.target.closest("[data-image-src]");
  if (!preview) return;
  openLightbox(preview.dataset.imageSrc, preview.dataset.imageTitle);
});

lightboxEls.closeButton.addEventListener("click", closeLightbox);
lightboxEls.modeButton.addEventListener("click", () => {
  setLightboxMode(state.lightboxMode === "fit" ? "width" : "fit");
});
lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) closeLightbox();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "/" && !event.metaKey && !event.ctrlKey && !event.altKey) {
    const tag = document.activeElement?.tagName?.toLowerCase();
    if (!["input", "textarea"].includes(tag)) {
      event.preventDefault();
      els.searchInput.focus();
    }
  }
  if (event.key === "Escape") {
    if (!lightbox.hidden) closeLightbox();
    closeSidebar();
  }
});

els.viewButton.addEventListener("click", () => setMode("view"));
els.editButton.addEventListener("click", () => setMode("edit"));
els.downloadButton.addEventListener("click", downloadCurrent);
els.copyButton.addEventListener("click", copyCurrent);
els.githubEditButton.addEventListener("click", () => {
  const doc = getDoc(state.currentId);
  window.open(`${REPO_EDIT_BASE}${encodeURIComponent(doc.path).replaceAll("%2F", "/")}`, "_blank", "noopener,noreferrer");
});
els.resetButton.addEventListener("click", () => {
  const doc = getDoc(state.currentId);
  resetContent(doc);
  renderDocument();
});
els.saveButton.addEventListener("click", () => {
  const doc = getDoc(state.currentId);
  setContent(doc, els.editor.value);
  renderDocument();
  setMode("edit");
});
els.editor.addEventListener("input", () => {
  const doc = getDoc(state.currentId);
  setContent(doc, els.editor.value);
});

renderDocument();
