USE pharmacy_db;

-- VIEW 1: STOCK SUMMARY
 --  create view vw_MonthlyInventoryReport as
--   select
--   p.ProductID,
--   p.CategoryName,
--   p.GenericName,
--   p.BrandName,
--   p.SellingPrice,
--  p.ReorderLevel,
--  coalesce(sum(b.QuantityRemaining),0) as TotalStock,
--  	case
--  		when coalesce(sum(b.QuantityRemaining),0) =0
--  			then 'Out of Stock'
--  		when coalesce(sum(b.QuantityRemaining),0) <=m.ReorderLevel
--  			then 'Low Stock'
--  		else 'In Stock'
--  	end as StockStatus
--  from Product p
--  left join Batch b on p.ProductID = b.ProductID
--  group by p.ProductID; 
 
-- NOTE
-- select GenericName, count(*) as count
-- from Medicine group by GenericName having Count > 1;

-- VIEW 2: EXPIRY ALERTS
-- create view vw_ExpiryAlerts as select
-- b.BatchID,
-- b.BatchNumber,
-- m.GenericName,
-- m.BrandName,
-- b.ExpiryDate,
-- b.QuantityRemaining,
-- datediff(b.ExpiryDate,current_date) as DaysUntilExpiry
-- from Batch b
-- join ProductID m on b.ProductID=m.ProductID
-- where b.ExpiryDate<=date_add(current_date, interval 90 day)
-- and b.QuantityRemaining > 0
-- order by b.ExpiryDate asc;
-- select * from vw_ExpiryAlerts;


-- VIEW 3: RECEIPT
-- create view vw_Receipt as select
-- sa.SaleID,
-- sa.SaleDate,
-- c.CustomerFName, c.CustomerSName,
-- st.StaffFName,st.StaffSName,
-- m.GenericName, m.BrandName,
-- si.QuantitySold, si.UnitPrice, si.Subtotal,
-- sa.TotalAmount, sa.PaymentMethod
-- from Sale sa
-- left join Customer c on sa.CustomerID = c.CustomerID
-- join Staff st on sa.StaffID=st.StaffID
-- join Sale_Item si on sa.SaleID=si.SaleID
-- join Batch b on si.BatchID=b.BatchID
-- join Product m on b.ProductID=m.ProductID;

-- set sql_safe_updates=0;

-- CREATE VIEW vw_PendingReorders AS
-- SELECT s.SuggestionID, p.BrandName, s.Last_Suggested_Date
-- FROM Reorder_Suggestion s
-- JOIN ProductID ON s.MedicineID = p.ProductID
-- WHERE s.SuggestionStatus = 'Pending';


-- CREATE OR REPLACE VIEW vw_DailySalesReport AS 
-- SELECT
--     sa.SaleID, sa.SaleDate,
--     p.GenericName, p.BrandName,
--     si.QuantitySold, sa.TotalAmount, 
--     sa.PaymentMethod, 
--     c.CustomerFName, c.CustomerSName,
--     st.StaffFName, st.StaffSName
-- FROM Sale sa
-- LEFT JOIN Customer c ON sa.CustomerID = c.CustomerID
-- JOIN Staff st ON sa.StaffID = st.StaffID
-- JOIN Sale_Item si ON sa.SaleID = si.SaleID
-- JOIN Batch b ON si.BatchID = b.BatchID
-- JOIN Product p ON b.ProductID = p.ProductID
-- WHERE sa.SaleDate = CURRENT_DATE;


-- CREATE OR REPLACE VIEW vw_MonthlySalesReport AS 
-- SELECT 
--      p.ProductID, p.GenericName, p.BrandName,
--      SUM(si.QuantitySold) AS TotalQuantitySold,
--      MONTHNAME(sa.SaleDate) AS SaleMonth
-- FROM Sale sa
-- JOIN Sale_Item si ON sa.SaleID = si.SaleID
-- JOIN Batch b ON si.BatchID = b.BatchID
-- JOIN Product p ON b.ProductID = p.ProductID
-- WHERE MONTH(sa.SaleDate) = MONTH(CURRENT_DATE) 
--    AND YEAR(sa.SaleDate) = YEAR(CURRENT_DATE)
-- GROUP BY p.ProductID, p.GenericName, p.BrandName, SaleMonth
-- ORDER BY TotalQuantitySold DESC;


-- CREATE OR REPLACE VIEW vw_Quarterly_Performance_Report AS
-- SELECT 
--     QUARTER(sa.SaleDate) AS SaleQuarter,
--     YEAR(sa.SaleDate) AS SaleYear,
--     p.ProductID, p.GenericName, p.BrandName,
--     SUM(si.QuantitySold) AS TotalQuantitySold
-- FROM Sale sa
-- JOIN Sale_Item si ON sa.SaleID = si.SaleID
-- JOIN Batch b ON si.BatchID = b.BatchID
-- JOIN Product p ON b.ProductID = p.ProductID
-- WHERE QUARTER(sa.SaleDate) = QUARTER(CURRENT_DATE)
--     AND YEAR(sa.SaleDate) = YEAR(CURRENT_DATE)
-- GROUP BY SaleYear, SaleQuarter, p.ProductID, p.GenericName, p.BrandName
-- ORDER BY TotalQuantitySold DESC;


-- CREATE OR REPLACE VIEW vw_ExpiryReport AS
-- SELECT 
--      p.GenericName, p.BrandName, 
--      b.BatchNumber, b.ExpiryDate, b.QuantityRemaining
-- FROM Batch b
-- JOIN Product p ON b.ProductID = p.ProductID
-- WHERE b.ExpiryDate BETWEEN CURRENT_DATE AND DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY)
--     AND b.QuantityRemaining > 0
-- ORDER BY b.ExpiryDate ASC;





-- CREATE OR REPLACE VIEW vw_DeliveryReport AS 
-- SELECT
--     d.DeliveryID, d.DeliveryDate, d.DeliveryStatus, d.DeliveryAddress,
--     c.CustomerFName, c.CustomerSName,
--     st.StaffFName, st.StaffSName,
--     p.GenericName, p.BrandName,
--     si.QuantitySold
-- FROM Delivery d
-- JOIN Sale sa ON d.SaleID = sa.SaleID
-- LEFT JOIN Customer c ON sa.CustomerID = c.CustomerID
-- JOIN Staff st ON d.StaffID = st.StaffID
-- JOIN Sale_Item si ON sa.SaleID = si.SaleID
-- JOIN Batch b ON si.BatchID = b.BatchID
-- JOIN Product p ON b.ProductID = p.ProductID
-- ORDER BY d.DeliveryDate ASC;


-- CREATE OR REPLACE VIEW vw_AnnualPerformanceReport AS
-- WITH Sales_Qty AS (
--     SELECT
--         YEAR(sa.SaleDate) AS ReportYear,
--         p.ProductID,
--         p.BrandName,
--         p.GenericName,
--         SUM(si.QuantitySold) AS TotalUnitsSold
--     FROM Product p
--     JOIN Batch b ON p.ProductID = b.ProductID
--     JOIN Sale_Item si ON b.BatchID = si.BatchID
--     JOIN Sale sa ON si.SaleID = sa.SaleID
--     GROUP BY YEAR(sa.SaleDate), p.ProductID, p.BrandName, p.GenericName
-- ),
-- Loss_Qty AS (
--     SELECT
--         YEAR(b.ExpiryDate) AS ReportYear,
--         b.ProductID,
--         SUM(b.QuantityRemaining) AS TotalUnitsExpired
--     FROM Batch b
--     WHERE b.ExpiryDate < CURRENT_DATE
--     AND b.QuantityRemaining > 0
--     GROUP BY YEAR(b.ExpiryDate), b.ProductID
-- )
-- SELECT
--     COALESCE(s.ReportYear, l.ReportYear) AS Year,
--     COALESCE(s.GenericName, p.GenericName) AS GenericName,
--     COALESCE(s.BrandName, p.BrandName) AS BrandName,
--     COALESCE(s.TotalUnitsSold, 0) AS TotalUnitsSold,
--     COALESCE(l.TotalUnitsExpired, 0) AS TotalUnitsExpired,
--     (COALESCE(s.TotalUnitsSold, 0) + COALESCE(l.TotalUnitsExpired, 0)) AS TotalMovement
-- FROM Sales_Qty s
-- LEFT JOIN Loss_Qty l ON s.ProductID = l.ProductID
--     AND s.ReportYear = l.ReportYear
-- LEFT JOIN Product p ON l.ProductID = p.ProductID
-- ORDER BY TotalUnitsSold DESC;


-- not in use
-- CREATE OR REPLACE VIEW vw_Annual_Performance_Report AS
-- WITH Sales_Qty AS (
--     SELECT 
--         YEAR(sa.SaleDate) AS ReportYear,
--         p.ProductID, p.BrandName,
--         SUM(si.QuantitySold) AS TotalUnitsSold
--     FROM Product p
--     JOIN Batch b ON p.ProductID = b.ProductID
--     JOIN Sale_Item si ON b.BatchID = si.BatchID
--     JOIN Sale sa ON si.SaleID = sa.SaleID
--     GROUP BY YEAR(sa.SaleDate), p.ProductID, p.BrandName
-- ),
-- Loss_Qty AS (
--     -- Combines Expiry from Batch and manual Adjustments (Damages/Returns)
--     SELECT 
--         YEAR(AdjustmentDate) AS ReportYear,
--         ProductID,
--         SUM(Quantity) AS TotalUnitsLost
--     FROM (
--         SELECT ExpiryDate AS AdjustmentDate, ProductID, QuantityRemaining AS Quantity 
--         FROM Batch WHERE ExpiryDate < CURRENT_DATE
--         UNION ALL
--         SELECT AdjustmentDate, ProductID, Quantity 
--         FROM Inventory_Adjustment -- Your table for damages/returns
--     ) AS CombinedLosses
--     GROUP BY YEAR(AdjustmentDate), ProductID
-- )

-- SELECT * FROM (
--     SELECT 
--         COALESCE(s.ReportYear, l.ReportYear) AS Year,
--         COALESCE(s.BrandName, (SELECT BrandName FROM Product WHERE ProductID = l.ProductID)) AS Product,
--         COALESCE(s.TotalUnitsSold, 0) AS UnitsSold,
--         COALESCE(l.TotalUnitsLost, 0) AS UnitsLost,
--         (COALESCE(s.TotalUnitsSold, 0) + COALESCE(l.TotalUnitsLost, 0)) AS TotalMovement
--     FROM Sales_Qty s
--     LEFT JOIN Loss_Qty l ON s.ProductID = l.ProductID AND s.ReportYear = l.ReportYear
--     UNION
--     SELECT 
--         COALESCE(s.ReportYear, l.ReportYear) AS Year,
--         (SELECT BrandName FROM Product WHERE ProductID = l.ProductID) AS Product,
--         COALESCE(s.TotalUnitsSold, 0) AS UnitsSold,
--         COALESCE(l.TotalUnitsLost, 0) AS UnitsLost,
--         (COALESCE(s.TotalUnitsSold, 0) + COALESCE(l.TotalUnitsLost, 0)) AS TotalMovement
--     FROM Sales_Qty s
--     RIGHT JOIN Loss_Qty l ON s.ProductID = l.ProductID AND s.ReportYear = l.ReportYear
-- ) AS FinalQtyReport
-- ORDER BY UnitsLost DESC;




