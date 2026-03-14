import json
import os
from csmar_client import CSMARClient

# ====== 你改这里 ======
CSMAR_ACCOUNT = "你的账号"
CSMAR_PASSWORD = "你的密码"

DEFAULT_EXPORT_DIR = os.path.expanduser("~/csmar_exports")
DEFAULT_PREVIEW_ROWS = 20
# =====================


def _ok(data):
    return {
        "success": True,
        "data": data
    }


def _err(message):
    return {
        "success": False,
        "error": message
    }


def _normalize_preview_rows(preview_rows):
    if preview_rows is None:
        return DEFAULT_PREVIEW_ROWS
    try:
        return int(preview_rows)
    except Exception:
        return DEFAULT_PREVIEW_ROWS


def _default_output_path(table_name: str, suffix: str = "csv"):
    os.makedirs(DEFAULT_EXPORT_DIR, exist_ok=True)
    return os.path.join(DEFAULT_EXPORT_DIR, f"{table_name}.{suffix}")


def run(
    action,
    database_name=None,
    table_name=None,
    columns=None,
    condition=None,
    start_time=None,
    end_time=None,
    output_path=None,
    preview_rows=20,
    file_format="csv"
):
    """
    Generic entry point for OpenClaw skill.

    Supported actions:
    - list_dbs
    - list_tables
    - list_fields
    - preview
    - query_data
    - download_data
    """

    if not action:
        return _err("action is required")

    preview_rows = _normalize_preview_rows(preview_rows)

    try:
        client = CSMARClient(CSMAR_ACCOUNT, CSMAR_PASSWORD)

        if action == "list_dbs":
            return _ok(client.list_dbs())

        if action == "list_tables":
            if not database_name:
                return _err("database_name is required for action=list_tables")
            return _ok(client.list_tables(database_name))

        if action == "list_fields":
            if not table_name:
                return _err("table_name is required for action=list_fields")
            return _ok(client.list_fields(table_name))

        if action == "preview":
            if not table_name:
                return _err("table_name is required for action=preview")
            data = client.preview(table_name)
            if isinstance(data, list):
                data = data[:preview_rows]
            return _ok(data)

        if action == "query_data":
            if not table_name:
                return _err("table_name is required for action=query_data")
            if not columns:
                return _err("columns is required for action=query_data")
            if condition is None:
                return _err("condition is required for action=query_data")

            df = client.query_data(
                columns=columns,
                condition=condition,
                table_name=table_name,
                start_time=start_time,
                end_time=end_time,
            )

            result = {
                "rows": int(len(df)),
                "columns": list(df.columns),
                "preview": df.head(preview_rows).to_dict(orient="records"),
            }

            if output_path:
                output_path = os.path.expanduser(output_path)
            else:
                suffix = "xlsx" if file_format.lower() == "xlsx" else "csv"
                output_path = _default_output_path(table_name, suffix=suffix)

            if file_format.lower() == "xlsx":
                saved_to = client.save_excel(df, output_path)
            else:
                saved_to = client.save_csv(df, output_path)

            result["saved_to"] = saved_to
            return _ok(result)

        if action == "download_data":
            if not table_name:
                return _err("table_name is required for action=download_data")
            if not columns:
                return _err("columns is required for action=download_data")
            if condition is None:
                return _err("condition is required for action=download_data")

            result = client.download_pack(
                columns=columns,
                condition=condition,
                table_name=table_name,
                start_time=start_time,
                end_time=end_time,
            )
            return _ok(result)

        return _err(f"unknown action: {action}")

    except Exception as e:
        return _err(str(e))


if __name__ == "__main__":
    # 方便你本地调试
    demo = run(action="list_dbs")
    print(json.dumps(demo, ensure_ascii=False, indent=2))