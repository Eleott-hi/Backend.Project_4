 DROP SCHEMA public CASCADE;
 CREATE SCHEMA public;

CREATE USER readonly_user WITH PASSWORD '1';
GRANT CONNECT ON DATABASE postgres TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_user;


-- Peers
CREATE TABLE IF NOT EXISTS peers
(
    nickname VARCHAR PRIMARY KEY,
    birthday DATE NOT NULL
);

-- IMPORT
CREATE OR REPLACE PROCEDURE prc_import_csv(p_table_name VARCHAR, p_columns VARCHAR, p_path VARCHAR, p_delimiter CHAR)
AS
$$
BEGIN
    EXECUTE concat('COPY ', p_table_name, ' ', p_columns,
                   ' FROM ', '''', p_path, p_table_name, '.csv', '''',
                   ' DELIMITER ''', p_delimiter, '''', ' CSV HEADER');
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE prc_export_csv(p_table_name VARCHAR, p_path VARCHAR, p_delimiter CHAR)
AS
$$
BEGIN
    EXECUTE concat('COPY ', p_table_name,
                   ' TO ', '''', p_path, p_table_name, '.csv', '''',
                   ' DELIMITER ''', p_delimiter, '''', ' CSV HEADER');
END;
$$ LANGUAGE plpgsql;

DO
$$
    DECLARE
        path VARCHAR := '/docker-entrypoint-initdb.d/datasets/';
    BEGIN
        CALL prc_import_csv('peers', '(nickname, birthday)', path, ',');
    END;
$$;