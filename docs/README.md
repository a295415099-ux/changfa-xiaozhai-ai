# GitHub Pages 发布说明

这个目录是「长发小寨 AI 总控工作台」的静态网站版本，适合直接部署到 GitHub Pages。

## 本站能做什么

- 在线阅读汇报文件、SOP、模板和总控说明。
- 搜索全部文档。
- 在网页里编辑 Markdown。
- 编辑内容会保存到当前浏览器的 localStorage。
- 支持复制当前文档 Markdown。
- 支持下载当前文档为 `.md` 文件。
- 支持跳转到 GitHub 网页编辑源文件。

## GitHub Pages 的限制

GitHub Pages 是静态网站。它可以展示页面，但不能在没有登录/API/后端的情况下，把网页里的编辑内容直接写回 GitHub 仓库。

如果需要“网页上点保存，所有人都能看到更新”，需要后续增加一种方案：

1. 接 GitHub OAuth + GitHub Contents API。
2. 接 Decap CMS / TinaCMS 等静态站 CMS。
3. 用一个小后端或 Serverless 函数处理保存。
4. 让团队直接在 GitHub 网页编辑 Markdown 源文件。

## 发布步骤

1. 把项目推到 GitHub 仓库。
2. 打开仓库 Settings。
3. 进入 Pages。
4. Source 选择 `Deploy from a branch`。
5. Branch 选择 `main`，目录选择 `/docs`。
6. 保存后等待 GitHub Pages 生成网址。

## 推荐工作流

- 日常阅读和临时修改：直接用网站编辑，复制或下载 Markdown。
- 正式更新：点击网站里的「GitHub编辑」修改源文件并提交。
- 多人协作：用 Pull Request 审核修改。
