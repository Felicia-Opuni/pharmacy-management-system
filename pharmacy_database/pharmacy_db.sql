USE pharmacy_db;

-- DROP VIEW IF EXISTS vw_MonthlyInventoryReport;
-- DROP VIEW IF EXISTS vw_ExpiryAlerts;
-- DROP VIEW IF EXISTS vw_Receipt;
-- DROP VIEW IF EXISTS vw_MonthlySalesReport;
-- DROP VIEW IF EXISTS vw_DailySalesReport;
-- DROP VIEW IF EXISTS vw_Quarterly_Performance_Report;
-- DROP VIEW IF EXISTS vw_ExpiryReport;
-- DROP VIEW IF EXISTS vw_Annual_Financial_Summary;
-- DROP VIEW IF EXISTS vw_PendingReorders;
-- DROP VIEW IF EXISTS vw_DeliveryReport;


-- DROP TRIGGER IF EXISTS trg_CalculateSubtotal;
-- DROP TRIGGER IF EXISTS trg_ReduceStock;
-- DROP TRIGGER IF EXISTS trg_UpdateTotalAmount;
-- DROP TRIGGER IF EXISTS trg_AfterSaleReturn;

-- DROP PROCEDURE IF EXISTS sp_GenerateReorderSuggestions;
-- DROP PROCEDURE IF EXISTS sp_ApproveSuggestion;
-- DROP PROCEDURE IF EXISTS sp_RejectSuggestion;


-- RENAME TABLE Medicine TO Product;


-- ALTER TABLE Product 
-- CHANGE MedicineID ProductID INT(5) NOT NULL AUTO_INCREMENT;

-- ALTER TABLE Batch 
-- CHANGE MedicineID ProductID INT(10) NOT NULL;

-- ALTER TABLE Purchase_Order_Item 
-- CHANGE MedicineID ProductID INT(10) NOT NULL;

-- ALTER TABLE Reorder_Suggestion 
-- CHANGE MedicineID ProductID INT(10) NOT NULL;


-- IVE DROPPED IT
-- CREATE PROCEDURE sp_ScanForLowStock()
-- BEGIN
--     -- Insert medicines that are low and NOT already pending or recently suggested
--     INSERT IGNORE INTO Reorder_Suggestion (MedicineID, Last_Suggested_Date, SuggestionStatus)
--     SELECT m.MedicineID, CURRENT_DATE, 'Pending'
--     FROM Medicine m
--     JOIN (
--         -- Calculate total stock across all batches for each medicine
--         SELECT MedicineID, SUM(QuantityRemaining) as TotalStock
--         FROM Batch
--         GROUP BY MedicineID
--     ) b ON m.MedicineID = b.MedicineID
--     WHERE b.TotalStock <= m.ReorderLevel;
-- END //

-- DELIMITER ;


-- DELIMITER //

-- IVE DROPPED IT
-- CREATE TRIGGER trg_UpdateStockAfterSale
-- AFTER INSERT ON Sale_Item
-- FOR EACH ROW
-- BEGIN
--     UPDATE Batch
--     SET QuantityRemaining = QuantityRemaining - NEW.QuantitySold
--     WHERE BatchID = NEW.BatchID;
-- END //

-- DELIMITER ;
show tables;