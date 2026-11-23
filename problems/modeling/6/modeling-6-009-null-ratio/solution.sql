SELECT COALESCE((COUNT(*)-COUNT(v))::numeric / NULLIF(COUNT(*),0),0) FROM readings;
