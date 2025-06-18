import sqlite3
from datetime import date


conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

while True:
    print("\n1. Додати замовлення\n2. Подивитись на загальний обсяг продажів\n3. Кількість замовлень на кожного клієнта\n4. Загальна кількість товарів кожної категорії\n5. Середній чек замовлення\n6. Найбільш популярна категорія товарів\n7. Вийти")
    choise = input("Оберіть опцію (1-7):")

    if choise == "0":
        # підвищення на 10%
        cursor.execute("""
            UPDATE products
            SET price = ROUND(price * 1.10)
            WHERE category = ?
        """, ("смартфони",))
        print("Ціна на смартфони піднята на 10%")
        conn.commit()

    if choise == "-0":
        # зменшення на 10%
        cursor.execute("""
            UPDATE products
            SET price = ROUND(price * 0.90)
            WHERE category = ?
        """, ("смартфони",))
        print("Ціна на смартфони зменшена на 10%")
        conn.commit()
    if choise == "1":
        #выбор клиента и добваление 
        cursor.execute("SELECT customer_id,first_name,last_name FROM customers ")
        for customer_id,first_name,last_name in cursor.fetchall():
            print(f"{customer_id}:{first_name,last_name}")
        customer_id = input("оберіть id клієнта: ")

        #вибір товара/скільки
        cursor.execute("SELECT product_id,name,price FROM products")
        for product_id,name,price in cursor.fetchall():
            print(f"{product_id}: {name,price}")
        product = input("оберіть id товару: ")
        cursor.execute("SELECT product_id FROM products WHERE product_id = ?",(product))
        product_1 = cursor.fetchall()
        if not product_1:
            print("такого id товару не існує!")
            continue
        quantity = input("кількість: ")

        order_date = date.today()
        
        save = input("Зберегти у базу данних? \n 1-так\n 2-ні ")

        if save =="1":
            cursor.execute("INSERT INTO orders (customer_id,product_id,quantity,order_date) VALUES (?,?,?,?)",(customer_id,product,quantity,order_date))
            conn.commit()
            print("інформація збережена ✅")
        if save == "2":
            print("збереження скасоване❌")

    if choise == "2":
        #обсяг продаж
        cursor.execute("""
            SELECT SUM(orders.quantity * products.price)
            FROM orders
            JOIN products ON orders.product_id = products.product_id;
        """)
        total = cursor.fetchone()
        print(f"Сумарний обсяг продажів: {total}")

    if choise == "3":
        #кількість замовлень на клиента 
        cursor.execute("""
            SELECT customers.customer_id , customers.first_name,customers.last_name, COUNT(orders.order_id) AS total_orders
            FROM customers
            LEFT JOIN orders ON customers.customer_id = orders.customer_id
            GROUP BY customers.customer_id;
        """)
        totals = cursor.fetchall()
        for total in totals:
            customer_id, first_name, last_name, total_orders = total
            print(f"{first_name} {last_name} (ID:{customer_id}) - замовлень: {total_orders}")

    if choise == "4":
        #усього товарів
        cursor.execute("""
            SELECT products.category, COUNT(*) AS total_category
            FROM products  
            GROUP BY products.category;
        """)
        
        totals = cursor.fetchall()
        for total in totals:
            category, total_category= total
            print(f"{category} - {total_category} товарів")

    if choise == "5":
        #середній чек
        cursor.execute("""
            SELECT AVG(products.price * orders.quantity) AS avg_check
            FROM orders
            JOIN products ON orders.product_id = products.product_id;
        """)
        totals = cursor.fetchone()
        avg_check = totals[0]
        print(f"Середня сумма чека: {avg_check:.2f} грн")

    if choise == "6":
        #Найбільш популярна категорія товарів
        cursor.execute("""
            SELECT products.category, COUNT(*) AS category_count
            FROM orders
            JOIN products ON orders.product_id = products.product_id
            GROUP BY products.category
            ORDER BY category_count DESC
        """)

        totals = cursor.fetchone()
        print(f"Найбільш популярна категорія товарів {totals} замовлень")

    if choise == "7":
        conn.close()
        break