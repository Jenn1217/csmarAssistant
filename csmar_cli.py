import argparse
import json
from csmar_skill import run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=[
        "list_dbs", "list_tables", "list_fields", "preview", "query_data", "download_data"
    ])
    parser.add_argument("--database_name")
    parser.add_argument("--table_name")
    parser.add_argument("--columns")
    parser.add_argument("--condition")
    parser.add_argument("--start_time")
    parser.add_argument("--end_time")
    parser.add_argument("--output_path")
    parser.add_argument("--preview_rows", type=int, default=20)
    parser.add_argument("--file_format", default="csv")

    args = parser.parse_args()

    columns = None
    if args.columns:
        columns = [c.strip() for c in args.columns.split(",") if c.strip()]

    result = run(
        action=args.action,
        database_name=args.database_name,
        table_name=args.table_name,
        columns=columns,
        condition=args.condition,
        start_time=args.start_time,
        end_time=args.end_time,
        output_path=args.output_path,
        preview_rows=args.preview_rows,
        file_format=args.file_format,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
