---
name: csmar-assistant
description: Query CSMAR databases, list tables and fields, preview data, run queries, and download packaged data.
homepage: https://data.csmar.com
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"]}}}
---

# CSMAR Assistant

Use CSMAR Python SDK to:

- list databases
- list tables under a database
- list fields of a table
- preview a table
- query data
- download packaged data

## Quick Commands

```bash
cd ~/.openclaw/skills/csmar-assistant

# list databases
python3 csmar_cli.py list_dbs

# list tables under a database
python3 csmar_cli.py list_tables --database_name "财务报表"

# list fields of a table
python3 csmar_cli.py list_fields --table_name "FS_Combas"

# preview a table
python3 csmar_cli.py preview --table_name "FS_Combas"

# query data
python3 csmar_cli.py query_data \
  --table_name "FS_Combas" \
  --columns "Stkcd,ShortName,Accper" \
  --condition "Stkcd='000001'" \
  --start_time "2020-01-01" \
  --end_time "2025-12-31"

# download packaged data
python3 csmar_cli.py download_data \
  --table_name "FS_Combas" \
  --columns "Stkcd,ShortName,Accper" \
  --condition "Stkcd like '3%'" \
  --start_time "2020-01-01" \
  --end_time "2025-12-31" '''EOF

