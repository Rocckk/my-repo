-- this script creates tables for db

CREATE DATABASE `url_getter`;

USE `url_getter`;

source ./schema/sources.sql;

source ./schema/urls.sql;

source ./schema/urls_to_sources.sql;

