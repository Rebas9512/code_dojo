CREATE VIEW registration_months AS
SELECT user_id, date_trunc('month', signup_date)::date AS cohort,
       (date_trunc('month', signup_date) + interval '1 month')::date AS next_start,
       (date_trunc('month', signup_date) + interval '2 months')::date AS next_end
FROM users;
