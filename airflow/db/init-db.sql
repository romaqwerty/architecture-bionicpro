CREATE DATABASE crm;
GRANT ALL PRIVILEGES ON DATABASE crm TO airflow;

\c crm
CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(50) UNIQUE
);

INSERT INTO users (id, username, date_of_birth, email) VALUES
('00000000-0000-0000-0000-000000000001', 'prothetic1', '1991-03-14', 'prothetic1@example.com'),
('00000000-0000-0000-0000-000000000002', 'prothetic2', '1988-07-22', 'prothetic2@example.com'),
('00000000-0000-0000-0000-000000000003', 'prothetic3', '1993-11-05', 'prothetic3@example.com');

CREATE DATABASE telemetry;
GRANT ALL PRIVILEGES ON DATABASE telemetry TO airflow;

\c telemetry

CREATE TABLE sensor_data (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    sensor_value NUMERIC
);

INSERT INTO sensor_data (user_id, timestamp, sensor_value) VALUES
('00000000-0000-0000-0000-000000000001', '2026-05-19 00:00:00', 13.8),
('00000000-0000-0000-0000-000000000002', '2026-05-19 00:01:00', 18.4),
('00000000-0000-0000-0000-000000000003', '2026-05-19 00:02:00', 24.1);

CREATE DATABASE olap;
GRANT ALL PRIVILEGES ON DATABASE olap TO airflow;

\c olap
CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    date_of_birth DATE,
    timestamp TIMESTAMP,
    sensor_value NUMERIC
);
