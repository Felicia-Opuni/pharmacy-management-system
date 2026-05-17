USE pharmacy_db;
-- CREATING TABLES

-- create table Medicine(
-- MedicineID int(5) not null auto_increment,
-- CategoryName varchar(100) not null,
-- GenericName varchar(100) not null,
-- BrandName varchar(100) not null,
-- SellingPrice decimal(10,2) not null,
-- ReorderLevel int(3) not null,
-- primary key(MedicineID)
-- );


-- create table Supplier (
-- SupplierID int(5) not null auto_increment,
-- SupplierName varchar(100) not null,
-- SupplierPhoneNumber varchar(15) not null,
-- SupplierEmail varchar(100) not null,
-- SupplierAddress varchar(150) not null,
-- primary key(SupplierID)
--  );

-- create table Staff(
-- StaffID int(5) not null auto_increment,
-- StaffFName varchar(100) not null,
-- StaffSName varchar(100) not null,
-- StaffPhoneNumber varchar(15) not null,
-- StaffEmail varchar(100) not null,
-- StaffAddress varchar(150) not null,
-- StaffRole varchar(100) not null,
-- primary key(StaffID)
-- );

-- create table Customer(
-- CustomerID int(5) not null auto_increment,
-- CustomerFName varchar(100) not null,
-- CustomerSName varchar(100) not null,
-- Gender varchar(30) not null check (Gender in ('Male','Female')),
-- DateOfBirth date not null,
-- CustomerPhoneNumber varchar(15) not null,
-- CustomerEmail varchar(100) null,
-- CustomerAddress varchar(150) not null,
-- CustomerHealthStatus varchar(50) not null,
-- primary key(CustomerID)
-- );


-- CREATING PURCHASE TABLE REFERENCING SUPPLIER TABLE

-- create table Purchase (
-- PurchaseID int(5) not null auto_increment,
-- SupplierID int(5) not null,
-- PurchaseDate date not null,
-- invioceNumber varchar(15) not null,
-- primary key(PurchaseID),
-- foreign key(SupplierID) references Supplier(SupplierID)
-- );
-- alter table Purchase
-- rename column invioceNumber to InvoiceNumber;

-- -- CREATING BATCH TABLE REFERENCING MEDICINE, PURCHASE TABLES

-- create table Batch(
-- BatchID int(5) not null auto_increment,
-- MedicineID int(5) not null,
-- PurchaseID int(5) not null,
-- BatchNumber varchar(15) not null,
-- ExpiryDate date not null,
-- ManufacturingDate date not null,
-- CostPrice decimal(10,2) not null,
-- QuantityRecieved int(10) not null,
-- QuantityRemaining int(10) not null,
-- primary key(BatchID),
-- foreign key(MedicineID) references Medicine(MedicineID),
-- foreign key(PurchaseID) references Purchase(PurchaseID)
-- );

-- alter table Batch
-- rename column QuantityRecieved to QuantityReceived ;

-- CREATING THE SALE TABLE REFERENCING CUSTOMER TABLE
-- create table Sale(
-- SaleID int(5) not null auto_increment,
-- StaffID int(5) not null,
-- CustomerID int(5) null,
-- SaleDate date not null,
-- TotalAmount decimal(10,2) not null,
-- PaymentMethod varchar(10) not null check(PaymentMethod in ('CASH','MOBILE MONEY')),
-- primary key (SaleID),
-- foreign key(CustomerID) references Customer(CustomerID),
-- foreign key (StaffID) references Staff(StaffID)
-- );

--  alter table Sale
--  drop constraint sale_chk_2;
-- modify column PaymentMethod varchar(30) not null,
-- add constraint chk_PaymentMethod check (PaymentMethod in ('Cash','MobileMoney'));


-- CREATING SALE ITEM TABLE REFERENCING SALE AND BATCH TABLE
-- create table Sale_Item(
-- SaleID int(5) not null,
-- BatchID int(5) not null,
-- QuantitySold int(10) not null,
-- UnitPrice decimal(10,2) not null,
-- Subtotal decimal(10,2) not null,
-- primary key(SaleID,BatchID),
-- foreign key(SaleID) references Sale(SaleID),
-- foreign key(BatchID) references Batch(BatchID)
-- );


-- CUSTOMER HEALTH RECORD TABLE REFERENCING CUSTOMER AND STAFF TABLES
-- create table Customer_Health_Record (
-- RecordID int(5) not null auto_increment,
-- CustomerID int(5) null,
-- StaffID int(5) not null,
-- VisitDate date not null,
-- NextVisitDate date null,
-- Symptoms varchar(255) not null,
-- Diagnosis varchar(255) not null,
-- ConsultationNotes varchar(255) not null,
-- primary key(RecordID),
-- foreign key(CustomerID) references Customer(CustomerID),
-- foreign key(StaffID) references Staff(StaffID)
-- );

-- alter table Customer_Health_Record
-- add column MedicationPrescribed varchar(255) null;
-- alter table Purchase_Order
-- add column TotalOrderAmount decimal(10,2) null;


-- CREATING PURCHASE ORDER TABLE REFERENCING SUPPLIER AND STAFF TABLES
-- create table Purchase_Order(
-- PurchaseOrderID int(5) not null auto_increment,
-- SupplierID int(5) not null,
-- StaffID int(5) not null,
-- OrderDate date not null,
-- ExpectedDeliveryDate date not null,
-- OrderStatus varchar(20) check(OrderStatus in ('Pending','Approved','Delivered')),
-- primary key(PurchaseOrderID),
-- foreign key(SupplierID) references Supplier(SupplierID),
-- foreign key(StaffID) references Staff(StaffID)
-- );

-- CREATING PURCHASE ORDER ITEM REFERENCING MEDICINE AND PURCHASE ORDER TABLE
-- drop table Purchase_Order_Item;
-- create  table Purchase_Order_Item(
-- OrderItemID INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
-- PurchaseOrderID int(5) null,
-- MedicineID int(5) not null,
-- QuantityOrdered int(10) not null,
-- foreign key(PurchaseOrderID) references Purchase_Order(PurchaseOrderID),
-- foreign key(MedicineID) references Medicine(MedicineID)
-- );


-- CREATING DELIVERY TABLE REFERENCING SALE AND STAFF TABLES
-- create table Delivery(
-- DeliveryID int(5) not null auto_increment,
-- SaleID int(5) not null,
-- StaffID int(5) not null,
-- DeliveryDate date not null,
-- DeliveryStatus varchar(20) not null check (DeliveryStatus in ('Pending','Approved','Delivered')),
-- DeliveryAddress varchar(150) not null,
-- primary key(DeliveryID),
-- foreign key(SaleID) references Sale(SaleID),
-- foreign key(StaffID) references Staff(StaffID)
-- );


-- CREATING REORDER SUGGESTION TABLE REFERENCING MEDICINE TABLE
-- create table Reorder_Suggestion(
-- SuggestionID int(5) not null auto_increment,
-- MedicineID int(5) not null,
-- SuggestionQuantity int(10) not null,
-- SuggestionDate date not null,
-- SuggestionStatus varchar(20) not null check(SuggestionStatus in ('Pending','Approved','Rejected')),
-- primary key(SuggestionID),
-- foreign key(MedicineID) references Medicine(MedicineID)
-- );
-- ALTER TABLE  Reorder_Suggestion
-- ADD COLUMN  RejectionReason VARCHAR(255)
-- RejectedDate



-- CREATE TABLE SALE RETURN REFERENCING SALE, BATCH,STAFF TABLES
-- CREATE TABLE Sale_Return (
--     ReturnID         INT(10)      NOT NULL AUTO_INCREMENT,
--     SaleID           INT(10)      NOT NULL,
--     BatchID          INT(10)      NOT NULL,
--     StaffID          INT(10)      NOT NULL,
--     ReturnDate       DATE         NOT NULL,
--     QuantityReturned INT(10)      NOT NULL,
--     Reason           VARCHAR(255) NULL,
--     PRIMARY KEY (ReturnID),
--     FOREIGN KEY (SaleID)  REFERENCES Sale(SaleID),
--     FOREIGN KEY (BatchID) REFERENCES Batch(BatchID),
--     FOREIGN KEY (StaffID) REFERENCES Staff(StaffID)
-- );

-- drop table Inventory_Adjustment;
-- CREATE TABLE Inventory_Adjustment (
--     AdjustmentID INT PRIMARY KEY AUTO_INCREMENT,
--     ProductID INT,
--     AdjustmentDate DATE,
--     Quantity INT,
--     Reason ENUM('Expired', 'Damaged', 'Returned-Waste', 'Theft'),
--     FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
-- );

-- ALTER TABLE Staff ADD COLUMN PasswordHash VARCHAR(255) NOT NULL;