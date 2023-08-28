import yaml
import os


with open(".config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

version = config["version"]

query = f"""
create application package if not exists connector_name;

use application package connector_name;

create schema if not exists app_schema;

use connector_name.app_schema;

create stage if not exists connector_name.app_schema.app_files
    file_format = ( type = 'csv' field_delimiter = '|' skip_header = 1);


-- Manifest file
put file://connector-name/manifest.yml
    @connector_name.app_schema.app_files/{version}
    overwrite=true auto_compress=false;

-- Readme
put file://connector-name/readme.md
    @connector_name.app_schema.app_files/{version}/connector-name/
    overwrite=true auto_compress=false;

-- Environment file
put file://connector-name/src/libraries/environment.yml
    @connector_name.app_schema.app_files/{version}/connector-name/src/libraries/
    overwrite=true auto_compress=false;

-- Python scripts
put file://connector-name/src/scripts/*.py
    @connector_name.app_schema.app_files/{version}/connector-name/src/scripts/
    overwrite=true auto_compress=false;

-- SQL scripts
put file://connector-name/src/scripts/*.sql
    @connector_name.app_schema.app_files/{version}/connector-name/src/scripts/
    overwrite=true auto_compress=false;

-- Libraries directory python files
put file://connector-name/src/libraries/*.py
    @connector_name.app_schema.app_files/{version}/connector-name/src/libraries/
    overwrite=true auto_compress=false;

-- Streamlit pages directory python files
put file://connector-name/src/libraries/pages/*.py
    @connector_name.app_schema.app_files/{version}/connector-name/src/libraries/pages
    overwrite=true auto_compress=false;
"""

os.system(
    f'snowsql -a  {config["account"]} -u {config["user"]} -r {config["role"]} -q "{query}"'
)
