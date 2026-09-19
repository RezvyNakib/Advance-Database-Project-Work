import sqlite3

conn = sqlite3.connect(r"E:\Advance Database\student_exchange_system\student_exchange.db")
c = conn.cursor()

print("=" * 60)
print("DATABASE: student_exchange.db")
print("=" * 60)

c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = c.fetchall()
print("\nTABLES:")
for t in tables:
    print(f"  - {t[0]}")

for table in ["University", "Coordinator", "Exchange_Program", "Student", "Student_Phone", "Application"]:
    print(f"\n--- {table} ---")
    c.execute(f"SELECT * FROM {table}")
    cols = [desc[0] for desc in c.description]
    print(f"  Columns: {cols}")
    for row in c.fetchall():
        print(f"  {row}")

conn.close()
