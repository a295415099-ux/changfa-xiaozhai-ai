import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const ROOT = process.cwd();
const OUTPUT_DIR = path.join(ROOT, "outputs");
const QR_PATH = path.join(ROOT, "assets/qr/changfa-ai-control-qr.png");
const PPTX_PATH = path.join(OUTPUT_DIR, "长发小寨AI总控台二维码单页.pptx");
const PNG_PATH = path.join(OUTPUT_DIR, "长发小寨AI总控台二维码单页.png");
const URL = "https://a295415099-ux.github.io/changfa-xiaozhai-ai/";

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

function addText(slide, text, position, style) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = style;
  return shape;
}

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });
  const qrBytes = await fs.readFile(QR_PATH);

  const deck = Presentation.create({
    slideSize: { width: 1280, height: 720 },
  });
  const slide = deck.slides.add();
  slide.background.fill = "#f6f4ef";

  slide.shapes.add({
    geometry: "rect",
    position: { left: 0, top: 0, width: 1280, height: 720 },
    fill: "#f6f4ef",
    line: { style: "solid", fill: "none", width: 0 },
  });
  slide.shapes.add({
    geometry: "rect",
    position: { left: 0, top: 0, width: 1280, height: 18 },
    fill: "#146c5c",
    line: { style: "solid", fill: "none", width: 0 },
  });
  slide.shapes.add({
    geometry: "rect",
    position: { left: 0, top: 660, width: 1280, height: 60 },
    fill: "#ebe6dc",
    line: { style: "solid", fill: "none", width: 0 },
  });

  addText(slide, "长发小寨 AI 总控工作台", { left: 82, top: 82, width: 640, height: 70 }, {
    fontSize: 46,
    bold: true,
    color: "#0f5148",
  });
  addText(slide, "品牌设计部 / 多 Agent 调度 / SOP 与项目资产库", { left: 86, top: 158, width: 650, height: 42 }, {
    fontSize: 22,
    color: "#687383",
  });

  const statement = "扫码进入总控台，查看 AI项目01、SOP泳道图、资料库、复盘表与后续所有 Agent 调度记录。";
  addText(slide, statement, { left: 86, top: 232, width: 590, height: 86 }, {
    fontSize: 25,
    color: "#1f2933",
  });

  const bullets = [
    "固定链接：二维码长期指向当前 GitHub Pages 总控台",
    "当前重点：高级感商详页 + 明星版本首页上线测试",
    "复盘方式：上市前基线数据 vs 上市后前 7 天数据",
  ];
  bullets.forEach((item, index) => {
    const y = 360 + index * 64;
    slide.shapes.add({
      geometry: "ellipse",
      position: { left: 92, top: y + 9, width: 18, height: 18 },
      fill: index === 0 ? "#146c5c" : index === 1 ? "#c99a3e" : "#b46a55",
      line: { style: "solid", fill: "none", width: 0 },
    });
    addText(slide, item, { left: 128, top: y, width: 620, height: 42 }, {
      fontSize: 20,
      color: "#303b47",
    });
  });

  slide.shapes.add({
    geometry: "roundRect",
    position: { left: 794, top: 82, width: 370, height: 482 },
    fill: "#fffdf8",
    line: { style: "solid", fill: "#d7d1c6", width: 1.5 },
    borderRadius: "rounded-2xl",
    shadow: "shadow-sm",
  });
  addText(slide, "扫码进入", { left: 844, top: 120, width: 270, height: 44 }, {
    fontSize: 32,
    bold: true,
    color: "#0f5148",
    alignment: "center",
  });
  slide.images.add({
    blob: qrBytes,
    contentType: "image/png",
    alt: "长发小寨 AI 总控工作台二维码",
    fit: "contain",
    position: { left: 860, top: 178, width: 240, height: 240 },
  });
  addText(slide, "长按识别 / 微信扫码", { left: 842, top: 438, width: 280, height: 32 }, {
    fontSize: 18,
    color: "#687383",
    alignment: "center",
  });
  addText(slide, URL, { left: 824, top: 492, width: 310, height: 42 }, {
    fontSize: 13,
    color: "#687383",
    alignment: "center",
  });

  addText(slide, "AI项目01：天猫首页及发膜0627设计初稿", { left: 86, top: 676, width: 540, height: 28 }, {
    fontSize: 16,
    bold: true,
    color: "#0f5148",
  });
  addText(slide, "长发小寨 · 史总汇报延展单页", { left: 914, top: 676, width: 270, height: 28 }, {
    fontSize: 16,
    color: "#687383",
    alignment: "right",
  });

  const png = await deck.export({ slide, format: "png", scale: 2 });
  await writeBlob(PNG_PATH, png);
  const pptx = await PresentationFile.exportPptx(deck);
  await pptx.save(PPTX_PATH);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
