USE pharmacy_db;
-- INSERTING MEDICINE DATA
-- INSERT INTO Medicine (CategoryName, GenericName, BrandName, SellingPrice, ReorderLevel)
-- VALUES 
-- ('Antibiotic',  'Amoxicillin',   'Amoxil',    5.50,  50),
-- ('Analgesic',   'Paracetamol',   'Panadol',   2.00,  100),
-- ('Antimalaria', 'Artemether',    'Coartem',   12.00, 30),
-- ('Vitamin',     'Ascorbic Acid', 'Vitamin C', 3.00,  80),
-- ('Antifungal',  'Fluconazole',   'Diflucan',  8.50,  20);

-- -- INSERTING SUPPLIER DATA
-- INSERT INTO Supplier (SupplierName, SupplierPhoneNumber, SupplierEmail, SupplierAddress)
-- VALUES
-- ('MedSupply Ghana Ltd', '0244000001', 'info@medsupply.gh',   'Accra, Ghana'),
-- ('PharmaDist Co.',      '0244000002', 'sales@pharmadist.gh', 'Kumasi, Ghana'),
-- ('HealthPlus Supplies', '0244000003', 'info@healthplus.gh',  'Takoradi, Ghana');

-- -- INSERTING STAFF DATA
-- INSERT INTO Staff (StaffFName, StaffSName, StaffPhoneNumber, StaffEmail, StaffAddress, StaffRole)
-- VALUES
-- ('Kofi',    'Mensah',   '0201000001', 'kofi@pharmacy.gh',    'Accra, Ghana',    'Pharmacist'),
-- ('Ama',     'Owusu',    '0201000002', 'ama@pharmacy.gh',     'Kumasi, Ghana',   'Cashier'),
-- ('Kwame',   'Asante',   '0201000003', 'kwame@pharmacy.gh',                  'Takoradi, Ghana', 'Delivery Rider'),
-- ('Abena',   'Boateng',  '0201000004', 'abena@pharmacy.gh',   'Accra, Ghana',    'Pharmacist'),
-- ('Yaw',     'Darko',    '0201000005', 'yaw@pharmacy.gh',                  'Accra, Ghana',    'Delivery Rider');
-- -- INSERTING CUSTOMER DATA
-- INSERT INTO Customer (CustomerFName, CustomerSName, Gender, DateOfBirth, CustomerPhoneNumber, CustomerEmail, CustomerAddress, CustomerHealthStatus)
-- VALUES
-- ('Akosua',  'Frimpong', 'Female', '1990-05-14', '0551000001', 'akosua@gmail.com',  'Accra, Ghana',    'Diabetic'),
-- ('Kweku',   'Acheampong','Male',  '1985-03-22', '0551000002', NULL,                'Kumasi, Ghana',   'Hypertensive'),
-- ('Efua',    'Mensah',   'Female', '2000-11-08', '0551000003', 'efua@gmail.com',    'Takoradi, Ghana', 'Healthy'),
-- ('Kojo',    'Asare',    'Male',   '1978-07-30', '0551000004', NULL,                'Accra, Ghana',    'Asthmatic'),
-- ('Adwoa',   'Boateng',  'Female', '1995-01-17', '0551000005', 'adwoa@gmail.com',   'Accra, Ghana',    'Healthy');
-- INSERTING PURCHASE DATA
-- INSERT INTO Purchase (SupplierID, PurchaseDate, InvoiceNumber)
-- VALUES
-- (1, '2026-01-10', 'INV-2026-001'),
-- (2, '2026-02-15', 'INV-2026-002'),
-- (3, '2026-03-20', 'INV-2026-003');
-- INSERTING BATCH DATA
-- INSERT INTO Batch (MedicineID, PurchaseID, BatchNumber, ExpiryDate, ManufacturingDate, CostPrice, QuantityReceived, QuantityRemaining)
-- VALUES
-- (1, 1, 'BT-AMX-001', '2026-07-01', '2025-07-01',3.00,  200, 45),
-- (2, 1, 'BT-PCM-001', '2026-10-01','2025-10-01', 1.00,  500, 120),
-- (3, 2, 'BT-ART-001', '2026-06-15', '2025-06-15',7.00,  100, 10),
-- (4, 2, 'BT-VTC-001', '2027-01-01', '2026-01-01',1.50,  300, 90),
-- (5, 3, 'BT-FLU-001', '2026-06-01',  '2025-06-01',5.00,  80,  5);


-- INSERTING SALE DATA

-- delete from Sale;
-- alter table Sale auto_increment=1;
-- INSERT INTO Sale (CustomerID, StaffID, SaleDate, TotalAmount, PaymentMethod)
-- VALUES
-- (1, 2, '2026-04-01', 11.00,  'Cash'),
-- (2, 2, '2026-04-05', 24.00,  'MobileMoney'),
-- (3, 4, '2026-04-10', 6.00,   'Cash'),
-- (NULL, 2, '2026-04-12', 17.00, 'MobileMoney'),
-- (5, 4, '2026-04-15', 8.50,   'Cash');

-- -- INSERTING SALE ITEM DATA
-- INSERT INTO Sale_Item (SaleID, BatchID, QuantitySold, UnitPrice, Subtotal)
-- VALUES
-- (1, 1, 2, 5.50,  11.00),
-- (2, 3, 2, 12.00, 24.00),
-- (3, 2, 3, 2.00,  6.00),
-- (4, 1, 1, 5.50,  5.50),
-- (4, 2, 1, 2.00,  2.00),
-- (5, 5, 1, 8.50,  8.50);
-- -- INSERTING CUSTOMER HEALTH RECORD DATA
-- INSERT INTO Customer_Health_Record (CustomerID, StaffID, VisitDate, NextVisitDate, Symptoms, Diagnosis, ConsultationNotes)
-- VALUES
-- (1, 1, '2026-04-01', '2026-07-01', 'High blood sugar',    'Diabetes Type 2',  'Prescribed Metformin'),
-- (2, 4, '2026-04-05', '2026-05-05', 'High blood pressure', 'Hypertension',     'Advised low salt diet'),
-- (3, 1, '2026-04-10', NULL,         'Fever and chills',    'Malaria',          'Prescribed Coartem'),
-- (4, 4, '2026-04-12', '2026-05-12', 'Shortness of breath', 'Asthma',          'Prescribed inhaler'),
-- (5, 1, '2026-04-15', NULL,         'Cough and cold',      'Upper Respiratory', 'Prescribe cough syrup');


-- INSERTING PURCHASE ORDER DATA
-- delete from Purchase_Order;
-- alter table Purchase_Order auto_increment=1;
-- INSERT INTO Purchase_Order (SupplierID, StaffID, OrderDate, ExpectedDeliveryDate, OrderStatus)
-- VALUES
-- (1, 1, '2026-04-01', '2026-04-10', 'Delivered'),
-- (2, 4, '2026-04-10', '2026-04-20', 'Approved'),
-- (3, 1, '2026-04-20', '2026-04-26',  'Pending');


-- INSERTING PURCHASE ORDER ITEM DATA
-- delete from Purchase_Order_Item;
-- INSERT INTO Purchase_Order_Item (PurchaseOrderID, MedicineID, QuantityOrdered)
-- VALUES
-- (1, 1, 200),
-- (1, 2, 500),
-- (2, 3, 100),
-- (2, 4, 300),
-- (3, 5, 80);




-- INSERTING DELIVERY DATA
-- INSERT INTO Delivery (SaleID, StaffID, DeliveryDate, DeliveryStatus, DeliveryAddress)
-- VALUES
-- (1, 3, '2026-04-02', 'Delivered', 'Accra, Ghana'),
-- (2, 5, '2026-04-06', 'Delivered', 'Kumasi, Ghana'),
-- (3, 3, '2026-04-11', 'Pending',   'Takoradi, Ghana'),
-- (4, 5, '2026-04-13', 'Approved',  'Accra, Ghana'),
-- (5, 3, '2026-04-16', 'Pending',   'Accra, Ghana');
-- -- INSERTING REORDER SUGGESTION DATA
-- INSERT INTO Reorder_Suggestion (MedicineID, SuggestionQuantity, SuggestionDate, SuggestionStatus)
-- VALUES
-- (1, 100, '2026-04-16', 'Pending'),
-- (3, 60,  '2026-04-16', 'Approved'),
-- (5, 40,  '2026-04-16', 'Pending');


show tables;
