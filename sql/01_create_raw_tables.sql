USE RetailPulse;
GO

-- Drop in correct order (dependencies)
IF OBJECT_ID('raw_order_items', 'U') IS NOT NULL DROP TABLE raw_order_items;
IF OBJECT_ID('raw_orders', 'U') IS NOT NULL DROP TABLE raw_orders;
IF OBJECT_ID('raw_products', 'U') IS NOT NULL DROP TABLE raw_products;
IF OBJECT_ID('raw_users', 'U') IS NOT NULL DROP TABLE raw_users;
GO

CREATE TABLE raw_users (
    user_id INT PRIMARY KEY,
    created_at DATETIME2 NOT NULL,
    country NVARCHAR(100) NOT NULL,
    city NVARCHAR(100) NOT NULL
);

CREATE TABLE raw_products (
    product_id INT PRIMARY KEY,
    category NVARCHAR(100) NOT NULL,
    product_name NVARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE raw_orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_datetime DATETIME2 NOT NULL,
    payment_method NVARCHAR(50) NOT NULL,
    status NVARCHAR(50) NOT NULL
);

CREATE TABLE raw_order_items (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    qty INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL
);
GO