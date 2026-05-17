USE pharmacy_db;

-- DELIMITER //

-- CREATE TRIGGER trg_CalculateSubtotal
-- BEFORE INSERT ON Sale_Item
-- FOR EACH ROW
-- BEGIN
--     SET NEW.Subtotal = NEW.QuantitySold * NEW.UnitPrice;
-- END //
-- DELIMITER ;
-- SHOW TRIGGERS IN pharmacy_db;


-- DELIMITER //
-- CREATE TRIGGER trg_ReduceStock
-- AFTER INSERT ON Sale_Item
-- FOR EACH ROW
-- BEGIN
--     UPDATE Batch
--     SET QuantityRemaining= QuantityRemaining - NEW.QuantitySold
--     WHERE BatchID = NEW.BatchID;
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE  TRIGGER trg_UpdateTotalAmount
-- AFTER INSERT ON Sale_Item
-- FOR EACH ROW
-- BEGIN
--     UPDATE Sale
--     SET TotalAmount  = (
--         SELECT SUM(Subtotal)
--         FROM Sale_Item
--         WHERE SaleID = NEW.SaleID
--     )
--     WHERE SaleID = NEW.SaleID;
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE TRIGGER trg_AfterSaleReturn
-- AFTER INSERT ON Sale_Return
-- FOR EACH ROW
-- BEGIN
--     -- Update 1: Increase stock
--     UPDATE Batch
--     SET QuantityRemaining = QuantityRemaining + NEW.QuantityReturned
--     WHERE BatchID  = NEW.BatchID;

--     -- Update 2: Reduce Sale_Item Subtotal
--     UPDATE Sale_Item
--     SET Subtotal = Subtotal - (NEW.QuantityReturned * Unitprice)
--     WHERE SaleID = NEW.SaleID
--     AND BatchID = NEW.BatchID;

--     -- Update 3: Recalculate TotalAmount in Sale
--     UPDATE Sale
--     SET TotalAmount = (
--         SELECT SUM(Subtotal)
--         FROM Sale_Item
--         WHERE SaleID = NEW.SaleID
--     )
--     WHERE SaleID = NEW.SaleID;
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE PROCEDURE sp_GenerateReorderSuggestions()
-- BEGIN
--     INSERT INTO Reorder_Suggestion 
--         (ProductID, SuggestionQuantity, SuggestionDate, SuggestionStatus)
--     SELECT
--         ProductID,
--         ReorderLevel,
--         CURRENT_DATE,
--         'Pending'
--     FROM vw_MonthlyInventoryReport
--     WHERE StockStatus = 'Low Stock'
--     AND ProductID NOT IN (
--         SELECT ProductID 
--         FROM Reorder_Suggestion 
--         WHERE SuggestionStatus = 'Pending'
--     );
-- END //
-- DELIMITER ;

-- CALL sp_GenerateReorderSuggestions();
-- SELECT * FROM Reorder_Suggestion;


-- DELIMITER //
-- CREATE PROCEDURE sp_ApproveSuggestion(IN p_SuggestionID INT)
-- BEGIN
--     -- Step 1: Insert into Purchase_Order_Item
--     INSERT INTO Purchase_Order_Item (PurchaseOrderID, ProductID, QuantityOrdered)
--     SELECT null, ID, SuggestionQuantity
--     FROM Reorder_Suggestion
--     WHERE SuggestionID = p_SuggestionID;

--     -- Step 2: Delete the suggestion
--     DELETE FROM Reorder_Suggestion
--     WHERE SuggestionID = p_SuggestionID;
-- END //
-- DELIMITER ;


-- DELIMITER //
-- CREATE PROCEDURE sp_RejectSuggestion(IN p_SuggestionID INT, IN p_RejectionReason VARCHAR(255))
-- BEGIN 
-- 	UPDATE Reorder_Suggestion
-- 	SET
-- 		SuggestionStatus = 'Rejected',
--         RejectionReason  = p_RejectionReason,
--         RejectedDate = current_date
--     WHERE SuggestionID = p_SuggestionID;
-- END //
-- DELIMITER ;


-- CREATE EVENT ev_DailyReorderCheck
-- ON SCHEDULE EVERY 1 DAY
-- STARTS '2026-05-05 07:00:00'
-- DO
-- CALL sp_GenerateReorderSuggestions();