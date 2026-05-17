# pharmacy-management-system

A full-stack database management system built to solve real problems 
in pharmacy operations — replacing paper-based records with a structured, 
automated digital system.

## 📌 Problem This Solves
- No early warning for expiring medicines
- Poor tracking of low stock and out-of-stock items
- Manual, error-prone supplier and sales reconciliation
- No structured customer health records

## 🛠️ Technologies Used
| Layer    | Technology               |
|----------|--------------------------|
| Database | MySQL                    |
| Backend  | Python, Flask            |
| Frontend | HTML, CSS, JavaScript    |

## 📂 Key Features
- **Inventory management** with automatic stock status (In Stock / Low Stock / Out of Stock)
- **Expiry alerts** — flags medicines expiring within 90 days
- **Automated reorder suggestions** generated daily by a scheduled event
- **Sales recording** with automatic stock deduction via triggers
- **Customer health records** linked to pharmacy visits
- **Delivery tracking** and sale returns
- **Role-based staff access** (Pharmacist, Cashier, Rider, CEO)

## 🗄️ Database Design
14 tables covering: Products, Batches, Sales, Suppliers, Staff, 
Customers, Health Records, Deliveries, Purchase Orders, and Returns.

Includes: Views, Triggers, Stored Procedures, and an Event Scheduler.

## 📊 Project Status
| Phase                | Status         |
|----------------------|----------------|
| Database (MySQL)     | ✅ Complete    |
| Backend (Flask API)  | ⏳ In Progress |
| Frontend             | ⏳ Coming Soon |

## 👩‍💻 About
Built as part of a BSc Information Technology Education project.
