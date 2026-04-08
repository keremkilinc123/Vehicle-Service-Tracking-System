import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql123",  # Sifren artik burada tanimli
        database="VehicleServiceDB"
    )

    cursor = db.cursor()

    # 1. Reset Database
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    tables = ["Payments", "ServiceRecords", "Services", "Technicians", "Vehicles", "Customers", "Users"]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    # 2. Create Tables
    cursor.execute("""
    CREATE TABLE Users (
        UserID INT PRIMARY KEY AUTO_INCREMENT,
        FullName VARCHAR(100),
        Email VARCHAR(100),
        Password VARCHAR(50),
        Role VARCHAR(20)
    )""")

    cursor.execute("""
    CREATE TABLE Customers (
        CustomerID INT PRIMARY KEY AUTO_INCREMENT,
        FullName VARCHAR(100),
        Phone VARCHAR(20),
        Email VARCHAR(100),
        Address TEXT
    )""")

    cursor.execute("""
    CREATE TABLE Vehicles (
        VehicleID INT PRIMARY KEY AUTO_INCREMENT,
        CustomerID INT,
        PlateNumber VARCHAR(20),
        Brand VARCHAR(50),
        Model VARCHAR(50),
        ModelYear INT,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE
    )""")

    cursor.execute("""
    CREATE TABLE Technicians (
        TechnicianID INT PRIMARY KEY AUTO_INCREMENT,
        FullName VARCHAR(100),
        Specialty VARCHAR(100),
        Phone VARCHAR(20)
    )""")

    cursor.execute("""
    CREATE TABLE Services (
        ServiceID INT PRIMARY KEY AUTO_INCREMENT,
        ServiceName VARCHAR(100),
        Description TEXT,
        UnitPrice DECIMAL(10,2)
    )""")

    cursor.execute("""
    CREATE TABLE ServiceRecords (
        RecordID INT PRIMARY KEY AUTO_INCREMENT,
        VehicleID INT,
        TechnicianID INT,
        ServiceDate DATE,
        Status VARCHAR(50),
        Notes TEXT,
        FOREIGN KEY (VehicleID) REFERENCES Vehicles(VehicleID),
        FOREIGN KEY (TechnicianID) REFERENCES Technicians(TechnicianID)
    )""")

    cursor.execute("""
    CREATE TABLE Payments (
        PaymentID INT PRIMARY KEY AUTO_INCREMENT,
        RecordID INT,
        PaymentDate DATE,
        Amount DECIMAL(10,2),
        PaymentMethod VARCHAR(50),
        FOREIGN KEY (RecordID) REFERENCES ServiceRecords(RecordID)
    )""")

    # 3. Insert Sample Data
    cursor.execute(
        "INSERT INTO Users (FullName, Email, Password, Role) VALUES ('Admin User', 'admin@mail.com', 'admin123', 'Admin')")
    cursor.execute(
        "INSERT INTO Customers (FullName, Phone, Email, Address) VALUES ('John Doe', '555-0101', 'john@mail.com', 'New York')")
    cursor.execute(
        "INSERT INTO Vehicles (CustomerID, PlateNumber, Brand, Model, ModelYear) VALUES (1, '34ABC123', 'Toyota', 'Corolla', 2020)")
    cursor.execute("INSERT INTO Technicians (FullName, Specialty, Phone) VALUES ('Alice Tech', 'Engine', '555-2001')")
    cursor.execute(
        "INSERT INTO Services (ServiceName, Description, UnitPrice) VALUES ('Oil Change', 'Replacing engine oil', 150.00)")

    db.commit()
    print("Database ready, tables created and sample data inserted!")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'db' in locals() and db.is_connected():
        db.close()




