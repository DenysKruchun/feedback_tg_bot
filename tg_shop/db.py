import sqlite3

def checking_user(tg_id):
    connection = sqlite3.connect("customer.db")
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM customer_info 
                   WHERE telegram_id = ?''',[tg_id])
    info_user = cursor.fetchone()
    connection.close()
    return info_user

def add_to_db(data):
    connection = sqlite3.connect("customer.db")
    cursor = connection.cursor()
    cursor.execute(''' INSERT INTO customer_info
                   VALUES(?,?,?,?,?)
                   ''', [data["full_name"], data['email'], data["rating"], data["text_feedback"], data["telegram_id"]])
    connection.commit()
    connection.close()

