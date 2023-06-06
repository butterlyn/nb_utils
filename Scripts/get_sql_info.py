# %%
# IMPORTS

import WA_db
import pandas as pd
import cx_Oracle

# %%
# GLOBAL VARIABLES

logger_name = __name__
logger_message_level = "DEBUG"
save_logfile = False


# %%
# Logger

from get_logger import get_logger

logger = get_logger(logger_name, logger_message_level, save_logfile)
logger.info("Logger initialised")

# %%
# HELPER FUNCTIONS


def _initialise_oracle_client(oracle_client_path: str) -> None:
    # initialse oracle client
    cx_Oracle.init_oracle_client(oracle_client_path)


def _get_sql_db_names() -> list:
    sql_db_names = list(WA_db.standard_dbs.keys())

    return sql_db_names


def _connect_to_sql_databases(sql_db_names: list) -> dict:
    sql_db_connection = {}

    for sql_db_name in sql_db_names[0:2]:
        try:
            sql_db_connection[sql_db_name] = WA_db.connect(db_name=sql_db_name)
            logger.info(f"Connected to {sql_db_name}")
        except cx_Oracle.DatabaseError as e:
            logger.error(f"Error connecting to {sql_db_name}: {e}")
            continue

    return sql_db_connection


logger.info(f"sql helper functions defined")

# %%
# COMPOSABLE FUNCTIONS


def connect_to_sql_databases(
    oracle_client_path: str = r"C:\Users\nbutterly\Oracle\instantclient_21_10",
) -> dict:
    _initialise_oracle_client(oracle_client_path)
    sql_db_names = _get_sql_db_names()
    sql_db_connection = _connect_to_sql_databases(sql_db_names)

    return sql_db_connection


logger.info("composable function defined")

# %%
# MODULE-LEVEL FUNCTION(S)


class SQLInfo:
    def __init__(
        self, oracle_client_path: str = r"C:\Users\nbutterly\Oracle\instantclient_21_10"
    ):
        self.oracle_client_path = oracle_client_path
        self.sql_db = self.connect_to_sql_databases()

    def connect_to_sql_databases(self) -> dict:
        _initialise_oracle_client(self.oracle_client_path)
        sql_db_names = _get_sql_db_names()
        sql_db_connection = _connect_to_sql_databases(sql_db_names)

        return sql_db_connection

    def get_sql_info(self, query: str, db_name: str = "WEMSDB") -> pd.DataFrame:
        sql_query_return = pd.read_sql(query, self.sql_db[db_name].db)
        return sql_query_return


logger.info("Module-level function(s) defined")


# %%
# MAIN

if __name__ == "__main__":
    logger.info("Running main")

    # set the sql query
    WEMSDB_query_1 = """SELECT
    f.facility_id,
    fc.short_name facility,
    pc.short_name participant,
    cr.effective_date facility_creation_date
FROM
    regn.facility_creation fc
    JOIN regn.facility f ON f.creation_id = fc.change_request_id
    JOIN regn.change_request cr ON cr.id = fc.change_request_id
    JOIN regn.participant p ON p.participant_id = fc.owner_id
    JOIN regn.participant_creation pc ON pc.change_request_id = p.creation_id
ORDER BY facility_creation_date
"""
    # set the sql database to connect to
    sql_info = SQLInfo()

    # get sql data and store in a dataframe
    df_sql_info = sql_info.get_sql_info(query=WEMSDB_query_1, db_name="WEMSDB")

    df_sql_info.shape
