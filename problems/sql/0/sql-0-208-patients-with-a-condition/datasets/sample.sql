CREATE TABLE patients (
    patient_id integer PRIMARY KEY,
    patient_name text NOT NULL,
    conditions text NOT NULL
);

INSERT INTO patients VALUES
    (4, '阿宁', 'DIAB100 R03'),
    (9, '阿蓝', 'G12 DIAB18'),
    (7, '子墨', 'XDIAB12'),
    (3, '许青', '');
