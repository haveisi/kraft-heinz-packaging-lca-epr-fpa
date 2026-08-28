-- Databricks notebook source
SELECT current_catalog() AS current_catalog,
       current_schema()  AS current_schema;

show catalogs;

create catalog if not exists kh_lca;

use catalog kh_lca;

select current_catalog();

CREATE SCHEMA IF NOT EXISTS kh_lca.bronze;

SHOW SCHEMAS IN kh_lca;

create schema if not exists kh_lca.silver;

create schema if not exists kh_lca.gold;

show schemas in kh_lca;

COMMENT ON SCHEMA kh_lca.bronze IS
'Raw source data for Kraft Heinz sustainability, LCA, financial, and emission factor analysis.';

COMMENT ON SCHEMA kh_lca.silver IS
'Cleaned, standardized, validated, and analysis-ready sustainability, LCA, and financial data.';

COMMENT ON SCHEMA kh_lca.gold IS
'Business-ready LCA, decarbonization, financial, scenario, and Power BI outputs.';

DESCRIBE SCHEMA EXTENDED kh_lca.bronze;

DESCRIBE SCHEMA EXTENDED kh_lca.silver;

DESCRIBE SCHEMA EXTENDED kh_lca.gold;

USE CATALOG kh_lca;
USE SCHEMA bronze;

SELECT
    current_catalog(),
    current_schema();


CREATE TABLE IF NOT EXISTS architecture_test (
    source_name STRING,
    reporting_year INT,
    value DOUBLE
);


INSERT INTO architecture_test
VALUES
    ('sustainability_report', 2022, 100.0),
    ('sustainability_report', 2023, 95.0),
    ('sustainability_report', 2024, 88.0);

SELECT *
FROM architecture_test;


TRUNCATE TABLE architecture_test;

INSERT INTO architecture_test
VALUES
    ('sustainability_report', 2022, 100.0),
    ('sustainability_report', 2023, 95.0),
    ('sustainability_report', 2024, 88.0);

SELECT *
FROM architecture_test;

SELECT COUNT(*) AS row_count
FROM architecture_test;


DESCRIBE TABLE architecture_test;

SELECT *
FROM kh_lca.bronze.architecture_test;




