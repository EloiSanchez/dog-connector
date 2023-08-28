create application role connector_name_role;

create schema if not exists code_schema;
grant usage on schema code_schema to application role connector_name_role;

-- Needed for streamlit app
create streamlit code_schema.connector_name_streamlit
    from 'connector-name/src/libraries/'
    main_file = '/Home.py';

grant usage on streamlit code_schema.connector_name_streamlit to application role connector_name_role;

create or replace table code_schema.logs (
    timestamp timestamp not null default current_timestamp(),
    session_id varchar default null,
    from_script varchar default null,
    level int not null,
    type varchar not null,
    message varchar not null
);
grant select on table code_schema.logs to application role connector_name_role;

insert into code_schema.logs(level, type, message)
    values (1, 'INFO', 'Connector Name application from Nimbus Intelligence has been installed');
