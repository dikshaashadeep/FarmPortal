import sqlite3

def init_db():
    conn = sqlite3.connect("farmportal.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id TEXT,
            animal_name TEXT,
            species TEXT,
            medicine TEXT,
            dose TEXT,
            reason TEXT,
            date_given TEXT,
            withdrawal_days INTEGER,
            safe_date TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id TEXT UNIQUE,
            name TEXT,
            species TEXT,
            breed TEXT,
            age TEXT,
            gender TEXT,
            owner TEXT,
            village TEXT,
            health_status TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users VALUES (NULL, 'farmer1', 'farm123', 'Farmer')")
        c.execute("INSERT INTO users VALUES (NULL, 'vet1', 'vet123', 'Veterinarian')")
        c.execute("INSERT INTO users VALUES (NULL, 'admin', 'admin123', 'Admin')")

    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect("farmportal.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def add_record(animal_id, animal_name, species, medicine_name, dose, reason, date_given, withdrawal_days, safe_date):
    conn = sqlite3.connect("farmportal.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO medicines
        (animal_id, animal_name, species, medicine, dose, reason, date_given, withdrawal_days, safe_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (animal_id, animal_name, species, medicine_name, dose, reason, date_given, withdrawal_days, safe_date))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect("farmportal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM medicines")
    data = c.fetchall()
    conn.close()
    return data

def add_animal(animal_id, name, species, breed, age, gender, owner, village="", health_status="Healthy"):
    conn = sqlite3.connect("farmportal.db")
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO animals (animal_id, name, species, breed, age, gender, owner, village, health_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (animal_id, name, species, breed, age, gender, owner, village, health_status))
        conn.commit()
        result = True
    except sqlite3.IntegrityError:
        result = False
    conn.close()
    return result

def get_all_animals():
    conn = sqlite3.connect("farmportal.db")
    c = conn.cursor()
    c.execute("SELECT * FROM animals")
    data = c.fetchall()
    conn.close()
    return data