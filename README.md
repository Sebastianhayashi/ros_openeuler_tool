# **ROS OpenEuler Tool**

## 🚀 **项目简介**

该工具是根据该[文章](https://github.com/Sebastianhayashi/openEuler-Jazzy-Porting/blob/main/Jazzy-porting-reports/Jazzy-porting-reports.md)中的内容所做的一个工具。

**ROS OpenEuler Tool** 是一个旨在简化 **ROS Jazzy** 版本软件包在 **openEuler** 系统上的移植、打包和管理的工具集。该工具集成了多个自动化脚本，能够高效地处理 ROS 包的克隆、依赖分析、RPM 打包、YUM 映射、Gitee 仓库同步等任务，帮助开发者减少手动操作的繁琐步骤，实现一键式自动化管理。

---

## 📚 **功能特性**

### 1️⃣ **批量克隆 ROS Jazzy 仓库**
- **命令:** `rot clone-repos`
- **功能:** 自动从 ROS 官方索引页面 (`https://index.ros.org/`) 获取所有 ROS Jazzy 软件包的仓库链接，并批量克隆到本地。

---

### 2️⃣ **批量处理 ROS 包**
- **命令:** `rot batch-process`
- **功能:** 在本地批量处理 ROS 包，生成 RPM 规范文件，分析依赖关系，记录跳过的包和未解析的依赖项。

---

### 3️⃣ **列出缺失的依赖**
- **命令:** `rot list-missing`
- **功能:** 列出在依赖关系中解析失败或缺失的 ROS 软件包和依赖项。

---

### 4️⃣ **分析依赖关系**
- **命令:** `rot analyze-dependencies`
- **功能:** 分析软件包之间的依赖关系，并生成构建顺序图，确保正确的打包和安装流程。

---

### 5️⃣ **将 YUM 仓库映射到 rosdep** （TODO）
- **命令:** `rot map-yum-to-rosdep`
- **功能:** 将 YUM 上游仓库中的软件包映射到 ROS 的 `rosdep` YAML 文件中，实现统一的依赖管理。

---

### 6️⃣ **自动更新 YUM 映射**
- **命令:** `rot update-yum-and-mapping`
- **功能:** 自动更新 YUM 上游仓库并同步到 `rosdep` 映射文件中，确保依赖项始终保持最新状态。

---

### 7️⃣ **生成 RPM 规范文件并打包源码**
- **命令:** `rot process-packages`
- **功能:** 为 ROS 包自动生成 RPM 规范文件（spec），并打包完整的源码包，准备在 openEuler 构建机器上进行打包构建。

---

### 8️⃣ **同步源码到 Gitee**
- **命令:** `rot sync-gitee`
- **功能:** 将 ROS 软件包的源码同步到 **Gitee** 仓库，并附带详细的 `README.md` 文件。

---

### 9️⃣ **将 Gitee 仓库设为公开**
- **命令:** `rot make-public`
- **功能:** 将所有私人 Gitee 仓库批量设置为公开，方便团队协作和资源共享。

---

## 🛠️ 依赖
- Python >= 3.8
- click：命令行工具库
- requests：HTTP 请求库
- beautifulsoup4：网页解析库
- PyYAML：YAML 文件处理
- networkx：依赖关系图构建

## 💻 **安装**

### **1. 克隆仓库**

```bash
git clone https://github.com/yourusername/ros_openeuler_tool.git
cd ros_openeuler_tool
```

2. 安装工具

```
pip install .
```

3. 配置环境变量

该工具依赖 GITEE_TOKEN 访问 Gitee API，请在系统中设置环境变量：

```
export GITEE_TOKEN=your_gitee_token
```

可选： 如果您使用 Gitee 组织，请设置：

```
export GITEE_ORG=your_gitee_org
```

4. 验证安装

```
rot --help
```