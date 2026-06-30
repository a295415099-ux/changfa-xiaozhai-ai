const docs = window.CHANGFA_DOCS || [];
const REPO_EDIT_BASE = "https://github.com/a295415099-ux/changfa-xiaozhai-ai/edit/main/";
const state = {
  currentId: docs[0]?.id || null,
  mode: "view",
  query: "",
  lightboxMode: "fit",
};

const els = {
  docList: document.getElementById("docList"),
  docGroup: document.getElementById("docGroup"),
  docTitle: document.getElementById("docTitle"),
  reader: document.getElementById("reader"),
  editorPanel: document.getElementById("editorPanel"),
  editor: document.getElementById("editor"),
  searchInput: document.getElementById("searchInput"),
  viewButton: document.getElementById("viewButton"),
  editButton: document.getElementById("editButton"),
  copyButton: document.getElementById("copyButton"),
  downloadButton: document.getElementById("downloadButton"),
  githubEditButton: document.getElementById("githubEditButton"),
  resetButton: document.getElementById("resetButton"),
  saveButton: document.getElementById("saveButton"),
  saveStatus: document.getElementById("saveStatus"),
};

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
  return `changfa-doc:${id}`;
}

function getDoc(id) {
  return docs.find((doc) => doc.id === id) || docs[0];
}

function getContent(doc) {
  return localStorage.getItem(storageKey(doc.id)) || doc.markdown;
}

function setContent(doc, value) {
  localStorage.setItem(storageKey(doc.id), value);
  els.saveStatus.textContent = "已保存到当前浏览器";
}

function resetContent(doc) {
  localStorage.removeItem(storageKey(doc.id));
  els.saveStatus.textContent = "已恢复原文";
}

function escapeHtml(value) {
  return String(value)
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
  if (rows.length < 2 || !/^\|[\s:-|]+\|$/.test(rows[1])) {
    return null;
  }
  const htmlRows = rows
    .filter((_, rowIndex) => rowIndex !== 1)
    .map((row, rowIndex) => {
      const cells = row
        .slice(1, -1)
        .split("|")
        .map((cell) => cell.trim());
      const tag = rowIndex === 0 ? "th" : "td";
      return `<tr>${cells.map((cell) => `<${tag}>${inlineMarkdown(cell)}</${tag}>`).join("")}</tr>`;
    })
    .join("");
  return { html: `<table>${htmlRows}</table>`, nextIndex: index };
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
  if (inCode) {
    html.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
  }
  return html.join("\n");
}

function groupDocs(filteredDocs) {
  return filteredDocs.reduce((groups, doc) => {
    if (!groups[doc.group]) groups[doc.group] = [];
    groups[doc.group].push(doc);
    return groups;
  }, {});
}

function renderNav() {
  const query = state.query.trim().toLowerCase();
  const filtered = docs.filter((doc) => {
    if (!query) return true;
    return `${doc.title} ${doc.group} ${doc.markdown}`.toLowerCase().includes(query);
  });
  const groups = groupDocs(filtered);
  els.docList.innerHTML = Object.entries(groups)
    .map(([group, groupDocs]) => {
      const buttons = groupDocs
        .map((doc) => {
          const selected = doc.id === state.currentId ? " selected" : "";
          return `<button class="doc-button${selected}" type="button" data-id="${doc.id}">${escapeHtml(doc.title)}</button>`;
        })
        .join("");
      return `<section><h3 class="group-title">${escapeHtml(group)}</h3>${buttons}</section>`;
    })
    .join("");
}

function renderDocument() {
  const doc = getDoc(state.currentId);
  const content = getContent(doc);
  state.currentId = doc.id;
  els.docGroup.textContent = doc.group;
  els.docTitle.textContent = doc.title;
  els.reader.innerHTML = markdownToHtml(content);
  els.editor.value = content;
  els.reader.hidden = state.mode !== "view";
  els.editorPanel.hidden = state.mode !== "edit";
  els.viewButton.classList.toggle("active", state.mode === "view");
  els.editButton.classList.toggle("active", state.mode === "edit");
  renderNav();
}

function setMode(mode) {
  state.mode = mode;
  renderDocument();
}

function downloadCurrent() {
  const doc = getDoc(state.currentId);
  const blob = new Blob([getContent(doc)], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${doc.title.replace(/[\\/:*?"<>|]/g, "-")}.md`;
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
  els.saveStatus.textContent = "已复制当前 Markdown";
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

els.docList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-id]");
  if (!button) return;
  state.currentId = button.dataset.id;
  els.saveStatus.textContent = "编辑会自动保存到当前浏览器";
  renderDocument();
});

els.searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderNav();
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
  if (event.key === "Escape" && !lightbox.hidden) closeLightbox();
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
