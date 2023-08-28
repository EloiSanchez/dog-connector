import yaml
import streamlit as st
from datetime import datetime
import random


@st.cache_resource
class Connection:
    def __init__(self) -> None:
        """Custom connection object that handles data transfer with Snowflake"""
        try:
            from snowflake.snowpark.context import get_active_session

            self.context = "Snowflake"

            self.session = get_active_session()
            self.session_identifier = self.session.get_session_stage().split("_")[
                -1
            ] + str(random.randint(100000, 999999))
            self.execute = lambda query: self.session.sql(query).collect()
            self.get_query = lambda query: self.session.sql(query).toPandas()
            self.close = lambda: self.session.close()

            self.info(
                "Connection",
                "Database connection has been created as session in Snowflake.",
            )
            self.debug("Connection", f"{self.session}")

        except ImportError:
            import snowflake.connector

            self.context = "Local"

            with open(".config.yml", "r") as config_file:
                config = yaml.safe_load(config_file)

            self.con = snowflake.connector.connect(
                user=config["user"],
                password=config["password"],
                account=config["account"],
                warehouse=config["warehouse"],
                database=config["database"],
                schema=config["schema"],
                role=config["role"],
            )
            self.session_identifier = "local connection"
            self.cur = self.con.cursor()
            self.execute = lambda query: self.cur.execute(query)
            self.get_query = lambda query: self.execute(query).fetch_pandas_all()
            self.close = lambda: self.con.close()

            self.info(
                "Connection",
                "Database connection has been created from local .config.yml file",
            )
            self.debug(
                "Connection",
                f"{config['account']=} {config['user']=} {config['warehouse']=} {config['database']=} {config['schema']=} {config['role']=}",
            )

    def _log(self, from_script: str, level: int, type_log: str, message: str) -> None:
        if self.context == "Snowflake":
            query = f"insert into code_schema.logs(session_id, from_script, level, type, message) values "
            query += f"('{self.session_identifier}', '{from_script}', {level}, '{type_log}', '{message}');"
            self.execute(query)
        elif self.context == "Local":
            print(
                f"{datetime.now()} - {self.session_identifier} - {from_script} - {type_log} - {message}"
            )
        else:
            raise ValueError(f"{self.context=} should be either 'Snowflake' or 'Local'")

    def debug(self, from_script: str, message: str) -> None:
        self._log(from_script, 0, "DEBUG", message)

    def info(self, from_script: str, message: str) -> None:
        self._log(from_script, 1, "INFO", message)

    def warning(self, from_script: str, message: str) -> None:
        self._log(from_script, 2, "WARNING", message)

    def error(self, from_script: str, message: str) -> None:
        self._log(from_script, 3, "ERROR", message)

    def create_env(self) -> None:
        self.info("Connection", "Creating database health_checks")
        self.execute("create database if not exists health_checks;")

    def clean_env(self) -> None:
        self.info("Connection", "Dropping database health_checks")
        self.execute("drop database if exists health_checks;")

    def reset_env(self) -> None:
        self.clean_env()
        self.create_env()
