import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

from calculations import *
from report_generator import generate_pdf
from excel_export import export_to_excel
from chart_generator import generate_chart
from calculations import design_status
# ==================== COLORS ====================
BG = "#1e1e1e"
TEXT = "white"
ACCENT = "#2e8b57"
FRAME_BG = "#252525"
HEADER_FG = "#00ccff"

# ==================== MAIN WINDOW ====================
root = tk.Tk()
root.title("Voltage Drop Calculator")
root.geometry("1100x850")
root.minsize(1000, 800)
root.resizable(True, True)
root.configure(bg=BG)

results = {}

# Top frame
top_frame = tk.Frame(root, bg=BG)
top_frame.pack(fill="x", padx=10, pady=5)

# ========================== PROJECT INFORMATION ==========================
project_frame = tk.LabelFrame(top_frame, text=" PROJECT INFORMATION ", 
                              font=("Arial", 9, "bold"), fg=HEADER_FG, 
                              bg=FRAME_BG, padx=8, pady=4)
project_frame.pack(side="left", fill="both", expand=True, padx=5)

row = 0
entries = {}
for label_text, default in [
    ("Project Name", "Office Building A"),
    ("Project Number", "P-001"),
    ("Client", "ABC Construction"),
    ("Engineer", "Mafizul Islam"),
    ("Date", datetime.now().strftime('%Y%m%d_%H%M%S'))
]:
    tk.Label(project_frame, text=label_text, bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(
        row=row, column=0, sticky="w", padx=8, pady=2)
    entry = tk.Entry(project_frame, width=35, font=("Arial", 9))
    entry.grid(row=row, column=1, padx=8, pady=2)
    entry.insert(0, default)
    entries[label_text.lower().replace(" ", "_")] = entry
    row += 1

project_name = entries["project_name"]
project_num = entries["project_number"]
client = entries["client"]
engineer = entries["engineer"]
date_entry = entries["date"]

# ========================== CALCULATION INPUTS ==========================

input_frame = tk.LabelFrame(top_frame, text=" CALCULATION INPUTS ", 
                            font=("Arial", 9, "bold"), fg=HEADER_FG, 
                            bg=FRAME_BG, padx=8, pady=4)
input_frame.pack(side="left", fill="both", expand=True, padx=5)

row = 0
tk.Label(input_frame, text="Diversity Factor (0.5 - 1)", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")

df_entry = tk.Entry(input_frame, width=22, font=("Arial", 9))
df_entry.insert(0, "0.6")
df_entry.grid(row=row, column=1, pady=2, padx=8)

row += 1

tk.Label(input_frame, text="Power (kW)", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")
power_entry = tk.Entry(input_frame, width=22, font=("Arial", 9))
power_entry.grid(row=row, column=1, pady=2, padx=8)
row += 1

tk.Label(input_frame, text="Voltage (V)", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")
voltage_entry = tk.Entry(input_frame, width=22, font=("Arial", 9))
voltage_entry.grid(row=row, column=1, pady=2, padx=8)
voltage_entry.insert(0, "400")
row += 1

tk.Label(input_frame, text="Power Factor", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")
pf_entry = tk.Entry(input_frame, width=22, font=("Arial", 9))
pf_entry.grid(row=row, column=1, pady=2, padx=8)
pf_entry.insert(0, "0.9")
row += 1

tk.Label(input_frame, text="Length (m)", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")
length_entry = tk.Entry(input_frame, width=22, font=("Arial", 9))
length_entry.grid(row=row, column=1, pady=2, padx=8)
row += 1

# Phase
tk.Label(input_frame, text="Phase", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")
phase_var = tk.StringVar(value="Three Phase")
phase_menu = tk.OptionMenu(input_frame, phase_var, "Single Phase", "Three Phase")
phase_menu.config(width=22, font=("Arial", 9))
phase_menu.grid(row=row, column=1, pady=2, padx=8, sticky="w")
row += 1

# Cable Material
tk.Label(input_frame, text="Cable Material", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")
material_var = tk.StringVar(value="Copper")
material_menu = tk.OptionMenu(input_frame, material_var, "Copper", "Aluminum")
material_menu.config(width=22, font=("Arial", 9))
material_menu.grid(row=row, column=1, pady=2, padx=8, sticky="w")
row += 1

# Installation Method
tk.Label(input_frame, text="Installation Method", bg=FRAME_BG, fg=TEXT, font=("Arial", 9, "bold")).grid(row=row, column=0, pady=2, padx=10, sticky="w")
install_var = tk.StringVar(value="Conduit")
install_menu = tk.OptionMenu(input_frame, install_var, "Conduit", "Cable Tray", "Buried", "Ladder")
install_menu.config(width=22, font=("Arial", 9))
install_menu.grid(row=row, column=1, pady=2, padx=8, sticky="w")

# ========================== RESULTS FRAME ==========================
result_frame = tk.LabelFrame(root, text=" RESULTS ", 
                             font=("Arial", 9, "bold"), fg=HEADER_FG, 
                             bg=FRAME_BG, padx=8, pady=4)
result_frame.pack(fill="both", expand=True, padx=10, pady=4)

result_label = tk.Label(
    result_frame,
    text="Results will appear here",
    font=("Segoe UI", 10),
    justify="left",
    bg="#111111",
    fg="white",
    relief="sunken",
    width=80,
    height=7,
    anchor="nw",
    padx=10,
    pady=6
)
result_label.pack(fill="both", expand=True, padx=5, pady=5)

# ========================== VOLTAGE DROP GAUGE ==========================
gauge = tk.Canvas(result_frame, width=700, height=120, bg="#111111", highlightthickness=0)
gauge.pack(pady=10)

def draw_gauge_base():
    """Draw the static parts of the gauge (called once)"""
    gauge.create_rectangle(20, 30, 200, 60, fill="#2ecc71", outline="")
    gauge.create_rectangle(200, 30, 320, 60, fill="#f1c40f", outline="")
    gauge.create_rectangle(320, 30, 620, 60, fill="#e74c3c", outline="")
    gauge.create_rectangle(20, 30, 620, 60, outline="white", width=2)
    
    gauge.create_text(20, 18, text="0%", fill="white")
    gauge.create_text(200, 18, text="3%", fill="white")
    gauge.create_text(320, 18, text="5%", fill="white")
    gauge.create_text(620, 18, text="10%", fill="white")
    
    gauge.create_text(110, 95, text="GOOD", fill="white", font=("Arial", 10, "bold"))
    gauge.create_text(260, 95, text="WARNING", fill="white", font=("Arial", 10, "bold"))
    gauge.create_text(470, 95, text="FAIL", fill="white", font=("Arial", 10, "bold"))

draw_gauge_base()

# ========================== CALCULATE FUNCTION ==========================
def calculate():
    global results

    try:
        power_input = power_entry.get().strip()

        if not power_input:
            return messagebox.showerror("Error", "Please enter at least one load")

        power_list = [float(p.strip()) for p in power_input.split(",") if p.strip()]

        # ================= INPUTS FIRST =================
        voltage = float(voltage_entry.get())
        pf = float(pf_entry.get())
        df = float(df_entry.get() if df_entry.get() else 0.6)
        length = float(length_entry.get())
        vd_limit = 5.0
        
        
        phase = phase_var.get()
        material = material_var.get()
        installation = install_var.get()
# ================= CALCULATIONS =================
        connected_power = sum(power_list)
        total_power = connected_power * df

        kva = total_power / pf
        kva_design = kva * 1.25

        try:
            transformer_size = select_transformer(kva_design)
        except:
            transformer_size = 100

        transformer_loading = (kva / transformer_size) * 100
        loading_status = transformer_status(transformer_loading)

        load_count = len(power_list)

        current = calculate_current(total_power, voltage, pf, phase)
        breaker = breaker_size(current)
        cable = recommend_cable(current, installation)

        
        resistance = 0.727 if material == "Copper" else 1.20
        vd = calculate_voltage_drop(current, length, resistance)
        vd_percent = (vd / voltage) * 100
        
        # Clear dynamic elements only
        gauge.delete("pointer")
        gauge.delete("value")
        gauge.delete("status")

        # Pointer position (capped at 10%)
        pointer_x = 20 + min(vd_percent, 10) * 60

        # Draw pointer
        gauge.create_line(pointer_x, 20, pointer_x, 75, fill="white", width=4, tags="pointer")

        # Voltage drop value
        gauge.create_text(320, 10, text=f"{vd_percent:.2f}% Voltage Drop",
                          fill="#00ccff", font=("Arial", 11, "bold"), tags="value")

        # Status
        status_text = "GOOD" if vd_percent <= 3 else "WARNING" if vd_percent <= 5 else "FAIL"
        status_color = "lime" if vd_percent <= 5 else "red"
        
        gauge.create_text(320, 115, text=status_text, fill=status_color,
                          font=("Arial", 11, "bold"), tags="status")

        # Update result label
        result_label.config(
            text=f"Current            : {current:.2f} A\n"
                 f"Voltage Drop       : {vd:.2f} V\n"
                 f"Voltage Drop %     : {vd_percent:.2f}%\n"
                 f"Cable Material     : {material}\n"
                 f"Installation       : {installation}\n"
                 f"Recommended Cable  : {cable} mm²\n"
                 f"Recommended Breaker: {breaker} A\n"
                 f"Status             : {status_text}\n"
                 f"Remarks            : {'Voltage drop is within IEC recommendations.' if vd_percent <= 5 else 'Voltage drop exceeds recommended limit.'}",
            fg=status_color
        )
              
        design_result = design_check(current, breaker, cable)
        print("DEBUG design_check return:", design_result)
        print("DEBUG type of return:", type(design_result))
        # === FIXED: Save results here (on successful calculation) ===
        results = {
            "kva": round(kva, 2),
            "kva_design": round(kva_design, 2),
            "project_name": project_name.get(),
            "project_number": project_num.get(),
            "client": client.get(),
            "engineer": engineer.get(),
            "date": date_entry.get(),

            "connected_power": connected_power,
            "diversity_factor": df,
            "power": total_power,
            "transformer_loading": round(transformer_loading, 1),
            "loading_status": loading_status,
            "load_count": load_count,
            "voltage": voltage,
            "pf": pf,
            "length": length,
            "transformer_size": transformer_size,
            "phase": phase,
            "material": material,
            "installation": installation,

            "current": current,
            "vd": vd,
            "vd_percent": vd_percent,

            "cable": cable,
            "breaker": breaker,

            "status": design_status(vd_percent, vd_limit),
            "design_check": design_check(current, breaker, cable),
            "remarks": "Voltage drop is within IEC recommendations." if vd_percent <= 5 else "Voltage drop exceeds recommended limit."
        }
        print("Results saved successfully:", results)
       

    except ValueError:
        result_label.config(text="Please enter valid numeric values.", fg="red")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}", fg="red")
        messagebox.showerror("Error", str(e))

# Export Functions (unchanged)
def export_pdf():
    if not results:
        return messagebox.showwarning("Warning", "Please click Calculate first!")
    try:
        print(results)
        print(type(results))
        
        generate_chart(results)
        
        file = generate_pdf(results)
        
        messagebox.showinfo("Success", f"PDF report generated!\n\n{file}")
    except Exception as e:
        messagebox.showerror("PDF Error", str(e))

def export_excel():
    if not results:
        return messagebox.showwarning("Warning", "Please click Calculate first!")
    try:
        file = export_to_excel(results)
        messagebox.showinfo("Success", f"Excel exported!\n\n{file}")
    except Exception as e:
        messagebox.showerror("Excel Error", str(e))

def create_chart():
    if not results:
        return messagebox.showwarning("Warning", "Please click Calculate first!")
    try:
        file = generate_chart(results)
        messagebox.showinfo("Success", f"Chart generated!\n\n{file}")
    except Exception as e:
        messagebox.showerror("Chart Error", str(e))

# Buttons
button_frame = tk.Frame(result_frame, bg=FRAME_BG)
button_frame.pack(side="bottom", pady=10)

for i, (text, cmd, color) in enumerate([
    ("Calculate", calculate, ACCENT),
    ("Export PDF", export_pdf, "#1f4e79"),
    ("Export Excel", export_excel, "#5a8f29"),
    ("Create Chart", create_chart, "#8b4513")
]):
    tk.Button(button_frame, text=text, command=cmd, bg=color, fg="white",
              font=("Arial", 10, "bold"), width=15, height=2).grid(row=0, column=i, padx=5)

root.mainloop()