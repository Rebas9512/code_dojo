INSERT INTO members SELECT id,tag FROM inbox
ON CONFLICT(id) /* 保留首次登记 */ ____;
