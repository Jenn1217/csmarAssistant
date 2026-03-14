import os
import pandas as pd
from csmarapi.CsmarService import CsmarService


class CSMARClient:
    def __init__(self, account: str, password: str):
        self.account = account
        self.password = password
        self.csmar = CsmarService()
        self._login()

    def _login(self):
        self.csmar.login(self.account, self.password)

    def list_dbs(self):
        return self.csmar.getListDbs()

    def list_tables(self, database_name: str):
        return self.csmar.getListTables(database_name)

    def list_fields(self, table_name: str):
        return self.csmar.getListFields(table_name)

    def preview(self, table_name: str):
        return self.csmar.preview(table_name)

    def query_data(
        self,
        columns,
        condition: str,
        table_name: str,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> pd.DataFrame:
        if start_time and end_time:
            df = self.csmar.query_df(columns, condition, table_name, start_time, end_time)
        else:
            df = self.csmar.query_df(columns, condition, table_name)

        if df is None:
            return pd.DataFrame()

        return df

    def query_count(
        self,
        columns,
        condition: str,
        table_name: str,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        if start_time and end_time:
            return self.csmar.queryCount(columns, condition, table_name, start_time, end_time)
        return self.csmar.queryCount(columns, condition, table_name)

    def save_csv(self, df: pd.DataFrame, output_path: str):
        output_path = os.path.expanduser(output_path)
        parent = os.path.dirname(output_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        df.to_csv(output_path, index=False)
        return output_path

    def save_excel(self, df: pd.DataFrame, output_path: str):
        output_path = os.path.expanduser(output_path)
        parent = os.path.dirname(output_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        df.to_excel(output_path, index=False)
        return output_path

    def download_pack(
        self,
        columns,
        condition: str,
        table_name: str,
        start_time: str | None = None,
        end_time: str | None = None,
    ):
        """
        Calls CSMAR packaged download.
        Note: your local CsmarService.py should already be modified for Mac/Linux paths.
        """
        if start_time and end_time:
            self.csmar.getPackResultExt(columns, condition, table_name, start_time, end_time)
        else:
            self.csmar.getPackResultExt(columns, condition, table_name)

        return {
            "status": "ok",
            "message": "Packaged download started/completed. Check your configured csmardata download folder."
        }