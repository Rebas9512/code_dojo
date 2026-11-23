INSERT INTO arrivals(sku,qty)
SELECT sku,qty FROM scans WHERE /* 只选择有效的到货行 */ ____;
