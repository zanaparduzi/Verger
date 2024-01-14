from flask import Flask, render_template, jsonify, session, request, redirect, url_for
import pymysql
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import mysql.connector
import os
from datetime import date

app = Flask(__name__)
app.secret_key = os.urandom(24)


# Function to establish a database connection
def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="new_password", database="Verger")

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='new_password',
    database='Verger'
)

cursor = db.cursor()

# Route to render index.html
@app.route('/')
def index():
    return render_template('choose.html', username=session.get('username'))
    #return render_template('products.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/facebook', methods=['GET', 'POST'])
def facebook():
    return render_template('facebook.html')

@app.route('/stock', methods=['POST'])
def stock():
    try:
        connection = get_db_connection()

        # Fetch data for Fruits table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Fruits")
            fruits_data = cursor.fetchall()

        # Fetch data for Legumes table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Legumes")
            legumes_data = cursor.fetchall()

        # Fetch data for Produits_Externes table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Produits_Externes")
            produits_externes_data = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Commandes_aux_Fournisseurs")
            commandes_fournisseurs_data = cursor.fetchall()

        return render_template('stock.html', fruits=fruits_data, legumes=legumes_data, produitsExternes=produits_externes_data,
                                commandesFournisseurs=commandes_fournisseurs_data)

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        connection.close()

@app.route('/nouvelle_vente', methods=['POST'])
def nouvelle_vente():
    try:
        connection = get_db_connection()

        # Fetch data for Fruits table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Fruits")
            fruits_data = cursor.fetchall()

        # Fetch data for Legumes table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Legumes")
            legumes_data = cursor.fetchall()

        # Fetch data for Produits_Externes table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Produits_Externes")
            produits_externes_data = cursor.fetchall()

        # Fetch sales data
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Sales")
            sales_data = cursor.fetchall()

        # Fetch data for Commandes_aux_Fournisseurs table
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Commandes_aux_Fournisseurs")
            commandes_fournisseurs_data = cursor.fetchall()

        return render_template('declarerVente.html', fruits=fruits_data, legumes=legumes_data, produitsExternes=produits_externes_data,
                                sales=sales_data, commandesFournisseurs=commandes_fournisseurs_data)

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        connection.close()


@app.route('/products')
def products():
    fruits_data = get_product_data("Fruits")
    legumes_data = get_product_data("Legumes")
    produits_externes_data = get_product_data("Produits_Externes")
    
    return render_template('products.html', fruits=fruits_data, legumes=legumes_data, produits_externes=produits_externes_data)

# Route to fetch table content
@app.route('/table/<table_name>')
def get_table_content(table_name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Create an HTML table to display the data
        table_html = "<table><tr>" + "".join(f"<th>{col}</th>" for col in columns) + "</tr>"
        for row in rows:
            table_html += "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
        table_html += "</table>"

        cursor.close()
        connection.close()

        return table_html

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/loyalclients', methods=['POST'])
def loyalclients():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Client")
            clients_data = cursor.fetchall()  # Fetch all data from the Client table

        connection.close()

        return render_template('loyalclients.html', clients=clients_data)

    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/login2',  methods=['POST'])
def login2():
    entered_username = request.form['username']
    entered_password = request.form['password']

    # Query to check credentials in the database
    sql = "SELECT * FROM Client WHERE username = %s AND password = %s"
    cursor.execute(sql, (entered_username, entered_password))
    user = cursor.fetchone()

    if user:
        username = user[1]
        password = user[9]
        admin = user[11]

        # If user exists in the database, redirect to OTP verification
        session['username'] = username
        session['password'] = password
        session['admin'] = admin


        if session['admin'] == True :
            return render_template('admin-interface.html', username=username)  # Page de vérification de l'OTP
        else :
            return redirect(url_for('products'))
    else:
        return "Invalid credentials. Please try again."

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html') 

@app.route('/register2', methods=['POST'])
def register2():
    username = request.form['username']
    name = request.form['name']
    surname = request.form['surname']
    password = request.form['password']
    email = request.form['email']
    phone = request.form['phone']

    # Insert data into the database
    sql = "INSERT INTO Client (username, Nom, Prenom, password, Email, Telephone) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (username, name, surname, password, email, phone)

    try:
        cursor.execute(sql, values)
        db.commit()
        #return render_template('login.html')
        return redirect('/login')  # Redirect to login page after successful registration
    except Exception as e:
        db.rollback()
        return "Error: " + str(e)
    
@app.route('/logout', methods=['GET','POST'])
def logout():
    return render_template('logout.html') 

'''@app.route('/reservations', methods=['GET','POST'])
def reservations():
    return render_template('reservations.html')'''


@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    try:
        client_id = request.args.get('client_id')

        if client_id is not None:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                # Fetch reservations for a specific client
                cursor.execute("SELECT * FROM Reservations WHERE ClientID = %s", (client_id,))
                reservations_data = cursor.fetchall()

            return render_template('reservations.html', reservations=reservations_data)

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        connection.close()

    # If no specific client_id is provided, fetch all reservations
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Reservations")
            reservations_data = cursor.fetchall()

        return render_template('reservations.html', reservations=reservations_data)

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        connection.close()


@app.route('/logout2', methods=['GET','POST'])
def logout2():
    # Vider toutes les variables de session
    session.clear()
    return redirect('/login')  # Rediriger vers la page de connexion après déconnexion

def get_product_data(table_name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        products_data = cursor.fetchall()
        cursor.close()
        connection.close()
        return products_data
    except Exception as e:
        return f"Error: {str(e)}"
    
# Function to get the client ID based on the username
def get_client_id(username):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID FROM Client WHERE username = %s", (username,))
            client_id = cursor.fetchone()[0]
        return client_id
    except Exception as e:
        raise e
    finally:
        connection.close()

# Route to handle reservation
@app.route('/reserve', methods=['POST'])
def reserve():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch remaining available quantity
        cursor.execute(f"SELECT Quantite_en_Stock FROM Fruits WHERE ID = {product_id}")
        remaining_quantity = cursor.fetchone()[0]

        # Check if requested quantity is valid
        if 1 <= quantity <= remaining_quantity:
            # Update the remaining quantity in the database
            cursor.execute(f"UPDATE Fruits SET Quantite_en_Stock = {remaining_quantity - quantity} WHERE ID = {product_id}")
            
            # Add a line in the Reservations table
            client_id = get_client_id(session['username'])
            cursor.execute("""
                INSERT INTO Reservations (ClientID, Produit, Quantite, Prix, DateAchat)
                SELECT %s, Nom_du_Produit, %s, Prix_Unitaire, NOW()
                FROM Fruits
                WHERE ID = %s
            """, (client_id, quantity, product_id))

            connection.commit()
            reservation_message = "Vous avez réservé ce produit"
        else:
            reservation_message = "Quantité invalide. Veuillez réessayer."

    except Exception as e:
        connection.rollback()
        reservation_message = f"Error: {str(e)}"
    finally:
        cursor.close()
        connection.close()

    fruits_data = get_product_data("Fruits")
    legumes_data = get_product_data("Legumes")
    produits_externes_data = get_product_data("Produits_Externes")

    return render_template('products.html', fruits=fruits_data, legumes=legumes_data, produits_externes=produits_externes_data, reservation_message=reservation_message)

@app.route('/declarer_vente')
def declarer_vente():
    return render_template('declarerVente.html')

@app.route('/validate_recovery/<int:reservation_id>', methods=['POST'])
def validate_recovery(reservation_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Get the product information and type associated with the reservation
        cursor.execute("""
            SELECT R.ID, R.Produit, R.Quantite, R.Prix, R.DateAchat, R.ClientID, R.Recupere,
                   CASE
                       WHEN F.ID IS NOT NULL THEN 'Fruit'
                       WHEN L.ID IS NOT NULL THEN 'Legume'
                       WHEN PE.ID IS NOT NULL THEN 'Produit_Externe'
                   END AS ProduitType
            FROM Reservations R
            LEFT JOIN Fruits F ON R.Produit = F.Nom_du_Produit
            LEFT JOIN Legumes L ON R.Produit = L.Nom_du_Produit
            LEFT JOIN Produits_Externes PE ON R.Produit = PE.Nom_du_Produit
            WHERE R.ID = %s
        """, (reservation_id,))
        reservation_info = cursor.fetchone()

        if reservation_info and not reservation_info[6]:  # Index 6 corresponds to 'Recupere'
            product_type = reservation_info[7]  # Index 7 corresponds to 'ProduitType'
            product_name = reservation_info[1]   # Index 1 corresponds to 'Produit'
            client_id = reservation_info[5]      # Index 5 corresponds to 'ClientID'

            # Update the 'Recupere' column in Reservations table to true
            cursor.execute("UPDATE Reservations SET Recupere = true WHERE ID = %s", (reservation_id,))

            # Update the 'Date_de_Vente' in the corresponding product table to today's date
            cursor.execute(f"UPDATE {product_type}s SET Date_de_Vente = %s WHERE Nom_du_Produit = %s", (date.today(), product_name))

            connection.commit()
            recovery_message = "Récupération validée avec succès!"
        else:
            recovery_message = "La récupération a déjà été validée ou la réservation n'existe pas."

    except Exception as e:
        connection.rollback()
        recovery_message = f"Erreur: {str(e)}"
    finally:
        cursor.close()
        connection.close()

    # Redirect back to the reservations page with a message
    return redirect(url_for('reservations', recovery_message=recovery_message))

@app.route('/declare_reception/<product_name>/<quantity_ordered>', methods=['POST'])
def declare_reception(product_name, quantity_ordered):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Update the 'Date_de_Reception' in the commandes_aux_fournisseurs table
        cursor.execute("""
            UPDATE Commandes_aux_Fournisseurs
            SET Date_de_Reception = CURDATE()
            WHERE Nom_du_Produit = %s AND Quantite_commandee = %s
        """, (product_name, quantity_ordered))

        # Search for the product in fruits, legumes, and produits_externes tables
        tables = ['Fruits', 'Legumes', 'Produits_Externes']
        for table in tables:
            cursor.execute(f"SELECT * FROM {table} WHERE Nom_du_Produit = %s", (product_name,))
            product = cursor.fetchone()

            if product:
                # Update the 'Quantite_en_Stock' and 'Date_de_Reception' in the corresponding table
                new_stock = product[2] + int(quantity_ordered)
                cursor.execute(f"UPDATE {table} SET Quantite_en_Stock = %s, Date_de_Reception = CURDATE() WHERE ID = %s", (new_stock, product[0]))

        connection.commit()

    except Exception as e:
        connection.rollback()
        return jsonify({'result': 'error', 'message': str(e)})
    finally:
        cursor.close()
        connection.close()

    return jsonify({'result': 'success'})

@app.route('/declareSale', methods=['POST'])
def declare_sale():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch product details
        cursor.execute("""
            SELECT F.ID, F.Nom_du_Produit, F.Quantite_en_Stock, F.Prix_Unitaire
            FROM Fruits F
            WHERE F.ID = %s

            UNION

            SELECT L.ID, L.Nom_du_Produit, L.Quantite_en_Stock, L.Prix_Unitaire
            FROM Legumes L
            WHERE L.ID = %s

            UNION

            SELECT PE.ID, PE.Nom_du_Produit, PE.Quantite_en_Stock, PE.Prix_Unitaire
            FROM Produits_Externes PE
            WHERE PE.ID = %s
        """, (product_id, product_id, product_id))

        product_info = cursor.fetchone()

        if product_info:
            product_id = product_info[0]
            product_name = product_info[1]
            current_quantity = product_info[2]
            product_price = product_info[3]

            # Check if requested quantity is valid
            if 1 <= quantity <= current_quantity:
                # Update the quantity in the corresponding table
                cursor.execute(f"UPDATE Fruits SET Quantite_en_Stock = {current_quantity - quantity} WHERE ID = {product_id}")
                
                # Add a line in the Sales table
                client_id = get_client_id(session['username'])
                cursor.execute("""
                    INSERT INTO Sales (ClientID, Produit, Quantite, Prix, DateVente)
                    VALUES (%s, %s, %s, %s, CURDATE())
                """, (client_id, product_name, quantity, product_price))

                connection.commit()
                sale_message = "Vente déclarée avec succès"
            else:
                sale_message = "Quantité invalide. Veuillez réessayer."
        else:
            sale_message = "Produit non trouvé. Veuillez réessayer."

        # Fetch product data after the sale
        fruits_data = get_product_data("Fruits")
        legumes_data = get_product_data("Legumes")
        produits_externes_data = get_product_data("Produits_Externes")

    except Exception as e:
        connection.rollback()
        sale_message = f"Erreur: {str(e)}"
    finally:
        cursor.close()
        connection.close()

    return render_template('declarerVente.html', fruits=fruits_data, legumes=legumes_data, produitsExternes=produits_externes_data, sale_message=sale_message)
if __name__ == '__main__':
    app.run(debug=True)
