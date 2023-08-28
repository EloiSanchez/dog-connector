# Developers README

## File Structure

```text
connector-name
├── .gitignore
├── .config.yml
├── README.md
└── connector-name
    └── src
        ├── libraries
        │   ├── Home.py
        │   ├── connection.py
        │   └── Pages
        │       └── **Pages for streamlit app if neeeded**
        ├── manifest.yml
        ├── readme.md
        └── scripts
            ├── upload_app.py
            └── setup.sql
```

## Set up environment

Create a new **Python 3.8** environment and activate it. For instance, with `venv`

```bash
python3.8 -m venv .venv
source .venv/bin/activate
```

and with `conda`, create a new `conda` environment and activate it

```bash
conda create --name <your_virt_env> python=3.8
conda activate <your_virt_env>
```

Install dependencies

```bash
pip install "snowflake-connector-python[pandas]"
pip install -r requirements.txt
```

Install pre-commit hooks

```bash
pre-commit install
```

## Uploading file package to Snowflake and testing in development

In order to test your current version of the code in Snowflake, run the `upload_app.py` script.

```bash
python connector-name/src/scripts/upload_app.py
```

This will upload the current files into an `APPLICATION PACKAGE` using the Snowflake account settings specified in the `.config.yml` file. Once the upload is finished, run the following command in Snowflake.

```sql
-- drop previous version of app if exists
drop application connector_name_app cascade;

-- create app from newly uploaded files
create APPLICATION connector_name_app
  from APPLICATION PACKAGE connector_name
  using '@connector_name.app_schema.app_files/<your_version>';

-- grant required privileges to app
grant create database on account to application connector_name_app;
```

## Testing a production version

Upload the files using the same script as in the previous section. **Make sure that you have updated the version in the config file**.

```sql
-- drop previous version of app if exists
drop application connector_name_app cascade;

-- create a version of the app
alter application package connector_name
  add version v1_1_0
  using '@connector_name.app_schema.app_files/v1.0.0'
  label = 'v1.1.0';

-- create app from newly uploaded files
create APPLICATION connector_name_app
  from APPLICATION PACKAGE connector_name
  using version v1_1_0;


-- grant required privileges to app
grant create database on account to application connector_name_app;
```

## Update requirements.txt

If you install any extra Python modules, make sure that they are [available in Snowflake](https://repo.anaconda.com/pkgs/snowflake/) and update the `requirements.txt` file accordingly.

## `.config.yml` file template

```yaml
# ./.config.yml

user: <user>
password: <password>
account: <account>
warehouse: health_check_wh
database: health_checks
schema: public
role: sysadmin
version: <name or whatever>_dev_v0.1.0  # For instance
```

## Best practices

- Commit on your own branch, never on main!
- Your branch should be named `<your-name>/<branch-name>`
- Write descriptive commit and pull requests messages, do not use commits as save-points
- Pull requests must be reviewed by another developer before merging
- Keep clean and commented code, apply Python and dbt best practices
- Include docstrings and type hinting to your Python functions
- Open issues in case there is any error / discussion / decision that requires collaboration. This ensures that we keep track of the project status and development
- Update the README.md with new information that must be know to developers that contribute to the repo
