import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Veritabanı bağlantısı
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql123",  # Kendi şifreni buraya yaz
        database="VehicleServiceDB"
    )

class VehicleServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Service Tracking System")
        self.root.geometry("1000x850")
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        self.login_page()

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def login_page(self):
        self.clear_screen()
        frame = tk.Frame(self.main_container)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame, text="SYSTEM LOGIN", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(frame, text="Email:").pack()
        self.ent_email = tk.Entry(frame, width=30)
        self.ent_email.insert(0, "admin@mail.com")
        self.ent_email.pack(pady=5)
        tk.Label(frame, text="Password:").pack()
        self.ent_pass = tk.Entry(frame, width=30, show="*")
        self.ent_pass.insert(0, "admin123")
        self.ent_pass.pack(pady=5)
        tk.Button(frame, text="Login", width=20, bg="#4CAF50", fg="white", command=self.handle_login).pack(pady=20)

    def handle_login(self):
        email, pw = self.ent_email.get(), self.ent_pass.get()
        try:
            db = get_connection()
            cursor = db.cursor()
            cursor.execute("SELECT FullName FROM Users WHERE Email=%s AND Password=%s", (email, pw))
            user = cursor.fetchone()
            if user:
                self.main_menu(user[0])
            else:
                messagebox.showerror("Error", "Invalid credentials!")
            db.close()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def main_menu(self, name):
        self.clear_screen()
        tk.Label(self.main_container, text=f"Welcome, {name}", font=("Arial", 14, "bold")).pack(pady=20)
        btn_frame = tk.Frame(self.main_container)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Customers & Vehicles", width=40, height=2, command=self.customer_page).pack(pady=5)
        tk.Button(btn_frame, text="Technicians & Services", width=40, height=2, command=self.tech_page).pack(pady=5)
        tk.Button(btn_frame, text="Service Records", width=40, height=2, command=self.service_page).pack(pady=5)
        tk.Button(btn_frame, text="Payments & Summary", width=40, height=2, command=self.payment_page).pack(pady=5)

        tk.Button(btn_frame, text="Logout", width=20, bg="#f44336", fg="white", command=self.login_page).pack(pady=30)

    # PAGE 2: CUSTOMERS & VEHICLES (FULL CRUD)
    def customer_page(self):
        self.clear_screen()
        tk.Button(self.main_container, text="< Back", command=lambda: self.main_menu("Admin")).pack(anchor="w", padx=10, pady=10)

        cf = tk.LabelFrame(self.main_container, text="Customer Management")
        cf.pack(fill="x", padx=20, pady=5)
        tk.Label(cf, text="Name:").grid(row=0, column=0)
        self.e_cn = tk.Entry(cf)
        self.e_cn.grid(row=0, column=1)
        tk.Label(cf, text="Phone:").grid(row=0, column=2)
        self.e_cp = tk.Entry(cf)
        self.e_cp.grid(row=0, column=3)
        tk.Button(cf, text="Save", bg="#4CAF50", fg="white", command=self.add_customer).grid(row=0, column=4, padx=5)
        tk.Button(cf, text="Update", bg="#2196F3", fg="white", command=self.update_customer).grid(row=0, column=5, padx=5)
        tk.Button(cf, text="Delete", bg="#f44336", fg="white", command=self.delete_customer).grid(row=0, column=6, padx=5)

        vf = tk.LabelFrame(self.main_container, text="Vehicle Management (Select Customer First)")
        vf.pack(fill="x", padx=20, pady=5)
        tk.Label(vf, text="Plate:").grid(row=0, column=0)
        self.e_vp = tk.Entry(vf)
        self.e_vp.grid(row=0, column=1)
        tk.Label(vf, text="Brand:").grid(row=0, column=2)
        self.e_vb = tk.Entry(vf)
        self.e_vb.grid(row=0, column=3)
        tk.Button(vf, text="Add", command=self.add_vehicle).grid(row=0, column=4, padx=2)
        tk.Button(vf, text="Update Plate", command=self.update_vehicle).grid(row=0, column=5, padx=2)
        tk.Button(vf, text="Delete Vehicle", command=self.delete_vehicle).grid(row=0, column=6, padx=2)

        self.ct = ttk.Treeview(self.main_container, columns=("ID", "Name", "Phone", "Plate", "Brand", "VID"), show='headings')
        for c in ("ID", "Name", "Phone", "Plate", "Brand", "VID"): self.ct.heading(c, text=c)
        self.ct.column("VID", width=0, stretch=tk.NO) # VID gizli kalsın
        self.ct.pack(fill="both", expand=True, padx=20)
        self.load_cv()

    def load_cv(self):
        for i in self.ct.get_children(): self.ct.delete(i)
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT c.CustomerID, c.FullName, c.Phone, v.PlateNumber, v.Brand, v.VehicleID FROM Customers c LEFT JOIN Vehicles v ON c.CustomerID = v.CustomerID")
        for r in cursor.fetchall(): self.ct.insert("", "end", values=r)
        db.close()

    def add_customer(self):
        db = get_connection(); cursor = db.cursor()
        cursor.execute("INSERT INTO Customers (FullName, Phone) VALUES (%s, %s)", (self.e_cn.get(), self.e_cp.get()))
        db.commit(); db.close(); self.load_cv()

    def update_customer(self):
        sel = self.ct.focus()
        if sel:
            cid = self.ct.item(sel)['values'][0]
            db = get_connection(); cursor = db.cursor()
            cursor.execute("UPDATE Customers SET FullName=%s, Phone=%s WHERE CustomerID=%s", (self.e_cn.get(), self.e_cp.get(), cid))
            db.commit(); db.close(); self.load_cv()

    def delete_customer(self):
        sel = self.ct.focus()
        if sel:
            cid = self.ct.item(sel)['values'][0]
            db = get_connection(); cursor = db.cursor()
            cursor.execute("DELETE FROM Customers WHERE CustomerID=%s", (cid,))
            db.commit(); db.close(); self.load_cv()

    def add_vehicle(self):
        sel = self.ct.focus(); cid = self.ct.item(sel)['values'][0] if sel else None
        if cid:
            db = get_connection(); cursor = db.cursor()
            cursor.execute("INSERT INTO Vehicles (CustomerID, PlateNumber, Brand) VALUES (%s, %s, %s)", (cid, self.e_vp.get(), self.e_vb.get()))
            db.commit(); db.close(); self.load_cv()

    def update_vehicle(self):
        sel = self.ct.focus(); vid = self.ct.item(sel)['values'][5] if sel else None
        if vid:
            db = get_connection(); cursor = db.cursor()
            cursor.execute("UPDATE Vehicles SET PlateNumber=%s, Brand=%s WHERE VehicleID=%s", (self.e_vp.get(), self.e_vb.get(), vid))
            db.commit(); db.close(); self.load_cv()

    def delete_vehicle(self):
        sel = self.ct.focus(); vid = self.ct.item(sel)['values'][5] if sel else None
        if vid:
            db = get_connection(); cursor = db.cursor()
            cursor.execute("DELETE FROM Vehicles WHERE VehicleID=%s", (vid,))
            db.commit(); db.close(); self.load_cv()

    # PAGE 3: TECHNICIANS (FULL CRUD)
    def tech_page(self):
        self.clear_screen()
        tk.Button(self.main_container, text="< Back", command=lambda: self.main_menu("Admin")).pack(anchor="w", padx=10, pady=10)
        tf = tk.LabelFrame(self.main_container, text="Technician Management")
        tf.pack(fill="x", padx=20, pady=5)
        tk.Label(tf, text="Name:").grid(row=0, column=0); self.e_tn = tk.Entry(tf); self.e_tn.grid(row=0, column=1)
        tk.Label(tf, text="Specialty:").grid(row=0, column=2); self.e_ts = tk.Entry(tf); self.e_ts.grid(row=0, column=3)
        tk.Button(tf, text="Add", bg="#4CAF50", fg="white", command=self.add_tech).grid(row=0, column=4, padx=2)
        tk.Button(tf, text="Update", bg="#2196F3", fg="white", command=self.update_tech).grid(row=0, column=5, padx=2)
        tk.Button(tf, text="Delete", bg="#f44336", fg="white", command=self.delete_tech).grid(row=0, column=6, padx=2)

        self.tt = ttk.Treeview(self.main_container, columns=("ID", "Name", "Specialty"), show='headings')
        for c in ("ID", "Name", "Specialty"): self.tt.heading(c, text=c)
        self.tt.pack(fill="both", expand=True, padx=20); self.load_techs()

    def load_techs(self):
        for i in self.tt.get_children(): self.tt.delete(i);
        db = get_connection(); cursor = db.cursor(); cursor.execute("SELECT TechnicianID, FullName, Specialty FROM Technicians")
        for r in cursor.fetchall(): self.tt.insert("", "end", values=r)
        db.close()

    def add_tech(self):
        db = get_connection(); cursor = db.cursor()
        cursor.execute("INSERT INTO Technicians (FullName, Specialty) VALUES (%s, %s)", (self.e_tn.get(), self.e_ts.get()))
        db.commit(); db.close(); self.load_techs()

    def update_tech(self):
        sel = self.tt.focus()
        if sel:
            tid = self.tt.item(sel)['values'][0]
            db = get_connection(); cursor = db.cursor()
            cursor.execute("UPDATE Technicians SET FullName=%s, Specialty=%s WHERE TechnicianID=%s", (self.e_tn.get(), self.e_ts.get(), tid))
            db.commit(); db.close(); self.load_techs()

    def delete_tech(self):
        sel = self.tt.focus()
        if sel:
            tid = self.tt.item(sel)['values'][0]
            db = get_connection(); cursor = db.cursor()
            cursor.execute("DELETE FROM Technicians WHERE TechnicianID=%s", (tid,))
            db.commit(); db.close(); self.load_techs()

    # PAGE 4: SERVICE RECORDS (CRUD)
    def service_page(self):
        self.clear_screen()
        tk.Button(self.main_container, text="< Back", command=lambda: self.main_menu("Admin")).pack(anchor="w", padx=10, pady=10)
        rf = tk.LabelFrame(self.main_container, text="Service Records")
        rf.pack(fill="x", padx=20, pady=5)

        db = get_connection(); cursor = db.cursor()
        cursor.execute("SELECT VehicleID, PlateNumber FROM Vehicles"); vs = cursor.fetchall()
        cursor.execute("SELECT TechnicianID, FullName FROM Technicians"); ts = cursor.fetchall(); db.close()

        tk.Label(rf, text="Vehicle:").grid(row=0, column=0)
        self.cb_v = ttk.Combobox(rf, values=[f"{v[0]}-{v[1]}" for v in vs]); self.cb_v.grid(row=0, column=1)
        tk.Label(rf, text="Tech:").grid(row=0, column=2)
        self.cb_t = ttk.Combobox(rf, values=[f"{t[0]}-{t[1]}" for t in ts]); self.cb_t.grid(row=0, column=3)
        tk.Button(rf, text="Create", bg="#4CAF50", fg="white", command=self.add_record).grid(row=0, column=4, padx=2)
        tk.Button(rf, text="Delete", bg="#f44336", fg="white", command=self.delete_record).grid(row=0, column=5, padx=2)

        self.rt = ttk.Treeview(self.main_container, columns=("ID", "Plate", "Tech", "Status"), show='headings')
        for c in ("ID", "Plate", "Tech", "Status"): self.rt.heading(c, text=c)
        self.rt.pack(fill="both", expand=True, padx=20); self.load_records()

    def load_records(self):
        for i in self.rt.get_children(): self.rt.delete(i)
        db = get_connection(); cursor = db.cursor()
        cursor.execute("SELECT r.RecordID, v.PlateNumber, t.FullName, r.Status FROM ServiceRecords r JOIN Vehicles v ON r.VehicleID=v.VehicleID JOIN Technicians t ON r.TechnicianID=t.TechnicianID")
        for r in cursor.fetchall(): self.rt.insert("", "end", values=r)
        db.close()

    def add_record(self):
        try:
            vid, tid = self.cb_v.get().split("-")[0], self.cb_t.get().split("-")[0]
            db = get_connection(); cursor = db.cursor()
            cursor.execute("INSERT INTO ServiceRecords (VehicleID, TechnicianID, ServiceDate, Status) VALUES (%s, %s, CURDATE(), 'Pending')", (vid, tid))
            db.commit(); db.close(); self.load_records()
        except: messagebox.showerror("Error", "Select fields!")

    def delete_record(self):
        sel = self.rt.focus()
        if sel:
            rid = self.rt.item(sel)['values'][0]
            db = get_connection(); cursor = db.cursor()
            cursor.execute("DELETE FROM ServiceRecords WHERE RecordID=%s", (rid,))
            db.commit(); db.close(); self.load_records()

    # PAGE 5: PAYMENTS & SUMMARY
    def payment_page(self):
        self.clear_screen()
        tk.Button(self.main_container, text="< Back", command=lambda: self.main_menu("Admin")).pack(anchor="w", padx=10, pady=10)
        db = get_connection(); cursor = db.cursor()
        cursor.execute("SELECT r.RecordID, v.PlateNumber FROM ServiceRecords r JOIN Vehicles v ON r.VehicleID=v.VehicleID WHERE r.Status='Pending'")
        recs = cursor.fetchall()
        cursor.execute("SELECT SUM(Amount) FROM Payments"); total = cursor.fetchone()[0] or 0; db.close()

        sf = tk.LabelFrame(self.main_container, text="Summary", bg="#e3f2fd"); sf.pack(fill="x", padx=20, pady=5)
        tk.Label(sf, text=f"Total Revenue: ${total}", font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=10)

        pf = tk.LabelFrame(self.main_container, text="Payment")
        pf.pack(fill="x", padx=20, pady=5)
        tk.Label(pf, text="Record:").grid(row=0, column=0); self.cb_r = ttk.Combobox(pf, values=[f"{r[0]}-{r[1]}" for r in recs]); self.cb_r.grid(row=0, column=1)
        tk.Label(pf, text="Amount:").grid(row=0, column=2); self.e_amt = tk.Entry(pf); self.e_amt.grid(row=0, column=3)
        tk.Button(pf, text="Save", command=self.add_payment).grid(row=0, column=4, padx=5)

        self.pt = ttk.Treeview(self.main_container, columns=("ID", "Record", "Date", "Amount"), show='headings')
        for c in ("ID", "Record", "Date", "Amount"): self.pt.heading(c, text=c)
        self.pt.pack(fill="both", expand=True, padx=20); self.load_payments()

    def load_payments(self):
        for i in self.pt.get_children(): self.pt.delete(i)
        db = get_connection(); cursor = db.cursor(); cursor.execute("SELECT PaymentID, RecordID, PaymentDate, Amount FROM Payments")
        for r in cursor.fetchall(): self.pt.insert("", "end", values=r)
        db.close()

    def add_payment(self):
        try:
            rid = self.cb_r.get().split("-")[0]
            db = get_connection(); cursor = db.cursor()
            cursor.execute("INSERT INTO Payments (RecordID, PaymentDate, Amount, PaymentMethod) VALUES (%s, CURDATE(), %s, 'Cash')", (rid, self.e_amt.get()))
            cursor.execute("UPDATE ServiceRecords SET Status='Completed' WHERE RecordID=%s", (rid,))
            db.commit(); db.close(); self.payment_page()
        except: messagebox.showerror("Error", "Check inputs!")

if __name__ == "__main__":
    root = tk.Tk(); app = VehicleServiceApp(root); root.mainloop()