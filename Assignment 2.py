import sqlite3
import socket
import random
from abc import ABC, abstractmethod


# ==========================================
# TASK 1: SQLite Database Operations
# ==========================================
def task1_sqlite_demo():
    print("=== TASK 1: SQLite Database Operations ===")
    try:
        # Connect to SQLite database (creates file if non-existent)
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')

        # Insert data
        sample_users = [
            ('Alice Smith', 'alice@example.com'),
            ('Bob Jones', 'bob@example.com')
        ]
        cursor.executemany(
            'INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)', 
            sample_users
        )
        conn.commit()

        # Retrieve and print data
        cursor.execute('SELECT * FROM users')
        records = cursor.fetchall()

        print("Database Records:")
        for row in records:
            print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
    print("\n" + "="*50 + "\n")


# ==========================================
# TASK 2: Encapsulation & BankAccount Class
# ==========================================
"""
CONCEPT EXPLANATION:
Encapsulation is an OOP principle that bundles data (attributes) and methods into a 
single unit (class) while restricting direct access to the internal state. In Python, 
encapsulation is achieved using naming conventions: double underscores (`__attribute`) 
trigger name-mangling to make attributes private and protect them from direct modification.
"""

class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0.0):
        self.owner = owner
        # Private attribute (Encapsulated)
        self.__balance = initial_balance

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__balance += amount
            print(f"Deposited ${amount:.2f}. New balance:${self.__balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            print("Withdrawal amount must be positive.")
        elif amount > self.__balance:
            print("Insufficient funds!")
        else:
            self.__balance -= amount
            print(f"Withdrew ${amount:.2f}. Remaining balance:${self.__balance:.2f}")

    def display_balance(self) -> None:
        print(f"Account Owner: {self.owner} | Current Balance: ${self.__balance:.2f}")


def task2_encapsulation_demo():
    print("=== TASK 2: Encapsulation Demo ===")
    account = BankAccount("John Doe", 100.0)
    account.display_balance()
    account.deposit(50.0)
    account.withdraw(30.0)

    # Demonstrating protection of private attribute
    try:
        print(account.__balance)
    except AttributeError:
        print("Direct access to '__balance' blocked. Encapsulation preserved!")
    print("\n" + "="*50 + "\n")


# ==========================================
# TASK 3: Socket Communication Demo
# ==========================================
def task3_socket_demo(host='127.0.0.1', port=65432):
    print("=== TASK 3: Client-Server Socket Communication ===")
    
    # Server side setup
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()

            # Client side connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))

                # Accept client on server
                conn, addr = server_socket.accept()
                with conn:
                    # Client sends message
                    message = "Hello from client!"
                    client_socket.sendall(message.encode('utf-8'))
                    
                    # Server receives message
                    data = conn.recv(1024)
                    print(f"Server received: {data.decode('utf-8')}")

    except socket.error as e:
        print(f"Socket Network Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    print("\n" + "="*50 + "\n")


# ==========================================
# TASK 4: Random Number Analysis
# ==========================================
def task4_random_demo():
    print("=== TASK 4: Random Numbers & Built-in Functions ===")
    # Generate 5 random floats between 0 and 10
    random_numbers = [random.uniform(0, 10) for _ in range(5)]
    
    print("Generated Numbers:")
    for num in random_numbers:
        print(f"  {num:.4f}")

    # Built-in min and max functions
    min_val = min(random_numbers)
    max_val = max(random_numbers)

    print(f"\nMinimum value: {min_val:.4f}")
    print(f"Maximum value: {max_val:.4f}")
    print("\n" + "="*50 + "\n")


# ==========================================
# TASK 5: Abstract Base Classes (ABC)
# ==========================================
class FileHandler(ABC):
    @abstractmethod
    def read(self, filepath: str) -> str:
        pass

    @abstractmethod
    def write(self, filepath: str, data: str) -> None:
        pass


class TextFileHandler(FileHandler):
    def read(self, filepath: str) -> str:
        return f"Reading plain text from '{filepath}'"

    def write(self, filepath: str, data: str) -> None:
        print(f"Writing text '{data}' into '{filepath}'")


class BinaryFileHandler(FileHandler):
    def read(self, filepath: str) -> str:
        return f"Reading binary stream from '{filepath}'"

    def write(self, filepath: str, data: str) -> None:
        print(f"Writing bytes '{data}' into '{filepath}'")


def task5_abc_demo():
    print("=== TASK 5: Abstract Base Class File Handlers ===")
    handlers = [TextFileHandler(), BinaryFileHandler()]
    
    for h in handlers:
        h.write("doc.dat", "Sample Data")
        print(h.read("doc.dat"))
    print("\n" + "="*50 + "\n")


# ==========================================
# TASK 6: Class Hierarchy & Method Overriding
# ==========================================
class Vehicle:
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model

    def start_engine(self) -> str:
        return f"The {self.brand} {self.model}'s engine starts."


class Car(Vehicle):
    def __init__(self, brand: str, model: str, num_doors: int):
        super().__init__(brand, model)
        self.num_doors = num_doors

    def start_engine(self) -> str:
        return f"The {self.brand} {self.model} (Car) starts smoothly with a push button."


class Bike(Vehicle):
    def __init__(self, brand: str, model: str, has_kickstart: bool):
        super().__init__(brand, model)
        self.has_kickstart = has_kickstart

    def start_engine(self) -> str:
        return f"The {self.brand} {self.model} (Bike) roars to life with a kickstart."


def task6_hierarchy_demo():
    print("=== TASK 6: Vehicle Inheritance & Overriding ===")
    fleet = [
        Vehicle("Generic", "Runner"),
        Car("Toyota", "Corolla", 4),
        Bike("Yamaha", "YZF", True)
    ]

    for vehicle in fleet:
        print(vehicle.start_engine())
    print("\n" + "="*50 + "\n")


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    task1_sqlite_demo()
    task2_encapsulation_demo()
    task3_socket_demo()
    task4_random_demo()
    task5_abc_demo()
    task6_hierarchy_demo()
