CREATE USER dbuser WITH PASSWORD 'dbpass';

-- Create tables
CREATE TABLE products (
                          product_sku VARCHAR(100) UNIQUE PRIMARY KEY,
                          product_name VARCHAR(255) NOT NULL,
                          product_description TEXT,
                          cost NUMERIC(10,2) NOT NULL,
                          category VARCHAR(100),
                          active BOOLEAN DEFAULT TRUE
);

CREATE TABLE stores (
                        store_id SERIAL PRIMARY KEY,
                        store_name VARCHAR(255) NOT NULL,
                        address_line1 VARCHAR(255) NOT NULL,
                        address_line2 VARCHAR(255),
                        city VARCHAR(100) NOT NULL,
                        state VARCHAR(100),
                        postal_code VARCHAR(20),
                        country VARCHAR(100) NOT NULL,
                        phone VARCHAR(50),
                        email VARCHAR(100)
);

CREATE TABLE customers (
                           customer_id SERIAL PRIMARY KEY,
                           first_name VARCHAR(100) NOT NULL,
                           last_name VARCHAR(100) NOT NULL,
                           email VARCHAR(255) UNIQUE NOT NULL,
                           phone VARCHAR(50),
                           address_line1 VARCHAR(255),
                           address_line2 VARCHAR(255),
                           city VARCHAR(100),
                           state VARCHAR(100),
                           postal_code VARCHAR(20),
                           country VARCHAR(100),
                           created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payment_methods (
                           customer_id SERIAL PRIMARY KEY REFERENCES customers(customer_id),
                           cc_num VARCHAR(16) NOT NULL,
                           exp_month VARCHAR(2) NOT NULL,
                           exp_year VARCHAR(4) NOT NULL,
                           cvc VARCHAR(4) NOT NULL
);

CREATE TABLE orders (
                        order_id SERIAL PRIMARY KEY,
                        customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
                        order_status VARCHAR(10) NOT NULL CHECK (order_status IN ('new', 'fulfilled')),
                        order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        store_id INTEGER REFERENCES stores(store_id),
                        total_amount NUMERIC(10,2),
                        payment_status VARCHAR(10) NOT NULL CHECK (payment_status IN ('unpaid', 'successful', 'failed')),
                        charge_token VARCHAR (500)
);

CREATE TABLE order_items (
                             order_item_id SERIAL PRIMARY KEY,
                             order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
                             product_sku VARCHAR(100) NOT NULL REFERENCES products(product_sku),
                             quantity INTEGER NOT NULL CHECK (quantity > 0),
                             unit_price NUMERIC(10,2) NOT NULL
);


CREATE TABLE inventory (
                           inventory_id SERIAL PRIMARY KEY,
                           product_sku VARCHAR(100) NOT NULL REFERENCES products(product_sku),
                           store_id INTEGER NOT NULL REFERENCES stores(store_id),
                           quantity INTEGER NOT NULL DEFAULT 0
);

ALTER TABLE inventory ADD CONSTRAINT unique_product_store UNIQUE (product_sku, store_id);

-- Add products
INSERT INTO products (product_name, product_description, cost, product_sku, category)
VALUES
    ('Ethiopian Light Roast', 'Fruity notes, ground coffee, 12oz bag', 12.99, 'COF-ETH-LG-12', 'Coffee Grounds'),
    ('Colombian Dark Roast', 'Bold, ground coffee, 12oz bag', 11.49, 'COF-COL-DR-12', 'Coffee Grounds'),
    ('French Press', 'Stainless steel, 1L capacity', 29.99, 'ACC-FRP-1L', 'Accessories'),
    ('Ceramic Mug', '12oz, white, company logo', 8.99, 'ACC-MUG-12', 'Drinkware'),
    ('Reusable Filter', 'Gold mesh filter, fits most drip machines', 7.49, 'ACC-FLT-RUS', 'Accessories'),
    ('Guatemalan Medium Roast', 'Balanced flavor, ground coffee, 12oz', 13.49, 'COF-GUA-MD-12', 'Coffee Grounds'),
    ('Travel Tumbler', '16oz, stainless steel', 19.99, 'ACC-TUM-16', 'Drinkware'),
    ('Cold Brew Kit', 'Starter kit for making cold brew at home', 24.99, 'KIT-CB-START', 'Kits'),
    ('Espresso Blend', 'Rich & bold, ground coffee, 12oz', 14.99, 'COF-ESP-12', 'Coffee Grounds'),
    ('Coffee Scoop', 'Stainless steel, 2 tbsp', 4.99, 'ACC-SCP-2TB', 'Accessories'),
    ('Organic Decaf', 'Swiss water process, ground, 12oz', 15.99, 'COF-DEC-ORG-12', 'Coffee Grounds'),
    ('Pour Over Set', 'Glass carafe, dripper, filters', 34.99, 'KIT-POUR-SET', 'Kits'),
    ('Classic Drip Machine', '12-cup programmable', 49.99, 'MAC-DRIP-12', 'Equipment'),
    ('Milk Frother', 'Handheld, battery powered', 12.49, 'ACC-FROTH-HH', 'Accessories'),
    ('Iced Coffee Glass', '16oz, clear glass', 9.99, 'ACC-GLS-16', 'Drinkware'),
    ('Costa Rican Single Origin', 'Bright acidity, ground, 12oz', 13.99, 'COF-CR-SO-12', 'Coffee Grounds'),
    ('Travel Mug', '20oz, spill proof lid', 17.99, 'ACC-TRAV-20', 'Drinkware'),
    ('Sustainable Tote Bag', 'Canvas, company logo', 14.99, 'ACC-TOTE', 'Merchandise'),
    ('Gift Card $25', 'Digital, for use online or in-store', 25.00, 'GIFTCARD25', 'Gift Cards'),
    ('Coffee Sampler Pack', '4x3oz bags, assorted', 19.99, 'KIT-SAMPLER', 'Kits'),
    ('Honduran Honey Process', 'Sweet notes, ground, 12oz', 13.49, 'COF-HON-HNY-12', 'Coffee Grounds'),
    ('Vietnamese Robusta', 'Strong, unique flavor, 12oz', 12.99, 'COF-VIE-ROB-12', 'Coffee Grounds'),
    ('Insulated Carafe', 'Keeps coffee hot, 1.5L', 27.99, 'ACC-CAR-15', 'Accessories'),
    ('Stovetop Espresso Maker', '6-cup, aluminum', 22.99, 'MAC-STOVE-6', 'Equipment'),
    ('Latte Art Pitcher', 'Stainless steel, 12oz', 15.49, 'ACC-PITCH-12', 'Accessories'),
    ('Nicaragua Single Origin', 'Nutty & smooth, ground, 12oz', 13.99, 'COF-NIC-SO-12', 'Coffee Grounds'),
    ('Mini French Press', '350ml, travel size', 17.49, 'ACC-FRP-MINI', 'Accessories'),
    ('Cold Brew Concentrate', '32oz, ready to drink', 11.99, 'COF-CB-CONC-32', 'Cold Brew'),
    ('Espresso Cups Set', '4x3oz, ceramic', 14.99, 'ACC-ESP-4SET', 'Drinkware'),
    ('Drip Coffee Filters', 'Pack of 100, unbleached', 5.99, 'ACC-FILT-100', 'Accessories'),
    ('House Blend', 'Signature blend, ground, 12oz', 11.99, 'COF-HOUSE-12', 'Coffee Grounds'),
    ('Coffee Grinder', 'Burr grinder, adjustable settings', 39.99, 'MAC-GRIND-BR', 'Equipment'),
    ('Brazilian Cerrado', 'Chocolatey notes, ground, 12oz', 12.49, 'COF-BRA-CER-12', 'Coffee Grounds'),
    ('Espresso Tamper', '58mm, stainless steel', 18.99, 'ACC-TAMP-58', 'Accessories'),
    ('Kenyan AA', 'Bright, complex, ground, 12oz', 14.49, 'COF-KEN-AA-12', 'Coffee Grounds'),
    ('Reusable Straw Set', '4 stainless steel, brush included', 9.49, 'ACC-STRAW-SET', 'Accessories'),
    ('Syrup Sampler', '3x2oz bottles (vanilla, caramel, hazelnut)', 8.99, 'KIT-SYRUP', 'Kits'),
    ('Mocha Mug', '16oz, ceramic', 10.99, 'ACC-MUG-MOCHA', 'Drinkware'),
    ('Hazelnut Flavored Coffee', 'Ground, 12oz', 13.99, 'COF-HAZ-12', 'Coffee Grounds'),
    ('Organic French Roast', 'Dark, ground, 12oz', 15.99, 'COF-FR-ORG-12', 'Coffee Grounds'),
    ('Glass Storage Jar', '1L, airtight lid', 13.49, 'ACC-JAR-1L', 'Accessories'),
    ('Digital Scale', 'Precision for brewing', 21.99, 'ACC-SCALE', 'Accessories'),
    ('Rwanda Bourbon', 'Berry notes, ground, 12oz', 13.99, 'COF-RWA-BRB-12', 'Coffee Grounds'),
    ('Vanilla Syrup', '12oz bottle', 7.99, 'ACC-SYRUP-VAN', 'Accessories'),
    ('Stainless Steel Filter', 'Reusable, pour over', 12.99, 'ACC-FLT-SS', 'Accessories'),
    ('Gift Card $50', 'Digital, for use online or in-store', 50.00, 'GIFTCARD50', 'Gift Cards'),
    ('Colombian Decaf', 'Smooth, ground, 12oz', 12.99, 'COF-COL-DEC-12', 'Coffee Grounds'),
    ('Signature Hoodie', 'M, black, company logo', 39.99, 'APP-HOOD-M', 'Apparel'),
    ('Signature Hoodie', 'L, black, company logo', 39.99, 'APP-HOOD-L', 'Apparel')
;

-- Add customers
INSERT INTO customers (first_name, last_name, email, phone, address_line1, city, state, postal_code, country)
VALUES
    ('John', 'Smith', 'john.smith@example.com', '555-1234', '101 Main St', 'Seattle', 'WA', '98101', 'USA'),
    ('Jane', 'Doe', 'jane.doe@example.com', '555-2345', '202 Oak Ave', 'Portland', 'OR', '97205', 'USA'),
    ('Carlos', 'Ramirez', 'carlos.ramirez@example.com', '555-3456', '303 Pine Rd', 'San Francisco', 'CA', '94109', 'USA'),
    ('Emily', 'Nguyen', 'emily.nguyen@example.com', '555-4567', '404 Maple St', 'Denver', 'CO', '80203', 'USA'),
    ('Ashley', 'Patel', 'ashley.patel@example.com', '555-5678', '505 Cedar Dr', 'Austin', 'TX', '78701', 'USA');

INSERT INTO payment_methods (customer_id, cc_num, exp_month, exp_year, cvc)
VALUES
    (1, '4242424242424242', '12', '2030', '123'),
    (2, '4111111111111111', '12', '2030', '123'),
    (3, '5555555555554444', '12', '2030', '123'),
    (4, '378282246310005', '12', '2030', '1234'),
    (5, '4000000000009995', '12', '2030', '123');

-- Add stores
INSERT INTO stores (store_name, address_line1, city, state, postal_code, country, phone)
VALUES
    ('Capitol Hill Coffee', '1415 Broadway', 'Seattle', 'WA', '98122', 'USA', '206-555-1111'),
    ('Mission Brews', '222 Valencia St', 'San Francisco', 'CA', '94110', 'USA', '415-555-2222'),
    ('Downtown Roast', '300 Main St', 'Chicago', 'IL', '60606', 'USA', '312-555-3333'),
    ('Sunset Espresso', '400 Ocean Ave', 'Los Angeles', 'CA', '90011', 'USA', '213-555-4444'),
    ('Riverfront Java', '123 River Rd', 'St. Louis', 'MO', '63101', 'USA', '314-555-5555');

-- Inventory for stores
-- add a random quantity of inventory for each store from 10 to 25
INSERT INTO inventory (product_sku, store_id, quantity)
SELECT product_sku, store_id, floor(random() * (25 - 10 + 1) + 10)::int
FROM products, stores;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dbuser;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to dbuser;