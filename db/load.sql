\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Category FROM 'Categories.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Inventory FROM 'Inventories.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY SavedItems FROM 'SavedItems.csv' WITH DELIMITER ',' NULL '' CSV;

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV;
