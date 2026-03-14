# CSMAR Assistant for OpenClaw

一个基于 **CSMAR Python SDK** 的 OpenClaw 自定义 skill，用于在 OpenClaw 中完成以下操作：

- 列出可访问的 CSMAR 数据库
- 列出某个数据库下的表
- 列出某张表的字段
- 预览表数据
- 查询指定条件下的数据
- 下载并打包数据

这个 skill 适合做金融研究、资产定价、A 股数据分析，以及后续构建本地量化研究数据仓库。

---

## 功能说明

当前支持以下动作：

- `list_dbs`
- `list_tables`
- `list_fields`
- `preview`
- `query_data`
- `download_data`

---

## 项目结构

```bash
csmar-assistant/
├── SKILL.md
├── _meta.json
├── csmar_client.py
├── csmar_skill.py
├── csmar_cli.py
└── csmar.sh
````

### 文件说明

* `SKILL.md`
  OpenClaw skill 描述文件

* `_meta.json`
  Skill 元信息文件

* `csmar_client.py`
  对 CSMAR SDK 的二次封装，提供统一接口

* `csmar_skill.py`
  Skill 核心逻辑入口，按 action 分发任务

* `csmar_cli.py`
  命令行调用入口，便于 OpenClaw 或终端直接调用

* `csmar.sh`
  指向指定 conda 环境 Python 的启动脚本，解决 OpenClaw 默认 Python 环境不一致的问题

---

## 环境要求

### 系统环境

* macOS / Linux / WSL
* Python 3.12（或你的实际可用版本）
* OpenClaw
* CSMAR Python SDK

### Python 依赖

```bash
pip install pandas urllib3 websocket-client prettytable
```

---

## CSMAR SDK 安装

由于 CSMAR SDK 不是公共 pip 包，需要手动安装。

你需要确保当前 Python 环境里可以成功执行：

```python
from csmarapi.CsmarService import CsmarService
```

如果你使用的是 conda 环境，可以通过以下命令检查：

```bash
python -c "from csmarapi.CsmarService import CsmarService; print('OK')"
```

如果输出 `OK`，说明 SDK 已正确安装。

---

## 安装步骤

### 1. 复制 skill 到 OpenClaw skills 目录

```bash
mkdir -p ~/.openclaw/skills
cp -R /你的路径/csmar-assistant ~/.openclaw/skills/
```

### 2. 确认 skill 目录结构正确

```bash
ls ~/.openclaw/skills/csmar-assistant
```

应至少包含：

```bash
SKILL.md
_meta.json
csmar_client.py
csmar_skill.py
csmar_cli.py
csmar.sh
```

### 3. 检查 OpenClaw 是否识别

```bash
openclaw skills
```

如果成功，你应该能在技能列表中看到 `csmar-assistant`。

---

## 配置账号

在 `csmar_skill.py` 中修改：

```python
CSMAR_ACCOUNT = "你的账号"
CSMAR_PASSWORD = "你的密码"
```

建议后续改为环境变量读取，而不是明文写死在代码里。

---

## 使用方法

### 1. 列出数据库

```bash
./csmar.sh list_dbs
```

### 2. 列出某个数据库下的表

```bash
./csmar.sh list_tables --database_name "财务报表"
```

### 3. 列出某张表的字段

```bash
./csmar.sh list_fields --table_name "FS_Combas"
```

### 4. 预览某张表

```bash
./csmar.sh preview --table_name "FS_Combas"
```

### 5. 查询数据

```bash
./csmar.sh query_data \
  --table_name "FS_Combas" \
  --columns "Stkcd,ShortName,Accper" \
  --condition "Stkcd='000001'" \
  --start_time "2020-01-01" \
  --end_time "2025-12-31"
```

### 6. 下载打包数据

```bash
./csmar.sh download_data \
  --table_name "FS_Combas" \
  --columns "Stkcd,ShortName,Accper" \
  --condition "Stkcd like '3%'" \
  --start_time "2020-01-01" \
  --end_time "2025-12-31"
```

---

## OpenClaw 中的推荐调用方式

由于当前 skill 还是“动作驱动”模式，所以建议这样调用：

* 使用 csmar-assistant，执行 list_dbs
* 使用 csmar-assistant，执行 list_tables，database_name 是 财务报表
* 使用 csmar-assistant，执行 list_fields，table_name 是 FS_Combas
* 使用 csmar-assistant，执行 query_data，table_name 是 FS_Combas，columns 是 Stkcd, ShortName, Accper，condition 是 Stkcd='000001'

不建议一开始就说：

* 帮我下载 2020-2025 年股票市场交易表

因为这句话对程序来说不够精确。
“股票市场交易”是数据库名，不是具体表名，仍然需要进一步定位表和字段。

---

## 返回结果与导出

### `query_data`

返回：

* 行数
* 字段列表
* 预览数据
* 保存路径

默认会导出为 CSV 到：

```bash
~/csmar_exports/
```

### `download_data`

调用 CSMAR 的打包下载接口，结果通常会保存到 SDK 配置的下载目录。

---

## 已知限制

### 1. 单次最多 200,000 行

CSMAR 的 `query` / `query_df` 有单次条数限制。
超过后需要分页查询，例如：

```text
limit 0,200000
limit 200000,200000
```

### 2. 相同查询条件 30 分钟限制

同一个 `condition + start_time + end_time` 组合，30 分钟内可能不能重复执行。

### 3. 依赖本地 CSMAR SDK

这个 skill 不是纯独立项目，必须依赖你本地可用的 `csmarapi`。

### 4. 当前仍属于“半结构化调用”

它更像一个“数据库操作 skill”，还不是完全自然语言智能代理。
也就是说，目前更适合：

* 先列库
* 再列表
* 再列字段
* 最后查询或下载

---

## 后续计划

后续可以继续增强：

* [ ] 自动分页下载
* [ ] 中文别名映射（如“资产负债表”→ `FS_Combas`）
* [ ] 自动识别常用股票市场交易表
* [ ] 结果直接写入 DuckDB / Parquet
* [ ] 环境变量管理账号密码
* [ ] 更自然的 OpenClaw 中文触发方式

---

## 适用场景

* A 股量化研究
* 资产定价数据准备
* 财务报表批量提取
* 股票市场交易数据下载
* OpenClaw 金融研究助手构建
* 本地 CSMAR 数据仓库前置工具

---

## 免责声明

本项目依赖用户合法可用的 CSMAR 账号与权限。
请遵守学校、数据库提供方以及相关服务条款，不要滥用接口或绕过授权限制。

---

## License

仅供学习、研究与个人使用。
如果你要公开分发，请确认不包含任何受限 SDK 文件或账号信息。
