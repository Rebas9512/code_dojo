CREATE VIEW open_jobs AS
SELECT id,fee FROM jobs WHERE /* 补上未结工单条件 */ ____;
