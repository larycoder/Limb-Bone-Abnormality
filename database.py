import mysql.connector as ketnoi

try:
    # Ket noi den phpMyAdmin
    con=ketnoi.connect(
        host='localhost',
        port='3307',
        user='root',
        password='',
        database='limbo'
    )

except Exception as e:
    print(f'Fail to connect: {e}')

sql=con.cursor()
def check(username,password):
    sql.execute(f"SELECT UserName, Password FROM sign_up WHERE UserName='{username}' AND Password='{password}'")
    ans=sql.fetchone()
    return ans is not None

def duplicate(username):
    sql.execute(f"SELECT UserName FROM sign_up WHERE UserName='{username}'")
    ans=sql.fetchone()
    return ans is None

def newUser(username,password):
    sql.execute(f"INSERT INTO sign_up(UserName, Password) VALUES('{username}','{password}')")
    con.commit()
    return sql.rowcount>0
# def sign_in(id,username,password):
