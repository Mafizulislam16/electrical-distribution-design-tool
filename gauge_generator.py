import matplotlib.pyplot as plt
import numpy as np
import os

def create_gauge(vd_percent):
    """Professional Semi-Circular Gauge - Optimized for PDF"""
    vd = min(float(vd_percent), 10)
    
    # Better size for PDF
    fig, ax = plt.subplots(figsize=(10, 6.8), dpi=320)
    fig.patch.set_facecolor('#111111')
    ax.set_facecolor('#111111')

    # Color and status
    if vd <= 3:
        ring_color = '#2ecc71'      # Green
        status = "EXCELLENT"
        status_color = '#2ecc71'
    elif vd <= 5:
        ring_color = '#f1c40f'      # Yellow
        status = "ACCEPTABLE"
        status_color = '#f1c40f'
    else:
        ring_color = '#e74c3c'      # Red
        status = "NON-COMPLIANT"
        status_color = '#e74c3c'

    # Semi-circular gauge
    sizes = [vd, 10 - vd]
    colors = [ring_color, '#2c3e50']
    
    ax.pie(sizes, colors=colors, startangle=180, 
           wedgeprops=dict(width=0.38, edgecolor='#111111', linewidth=5))

    # Center Value
    ax.text(0, 0.05, f"{vd:.2f}%", ha='center', va='center', 
            fontsize=38, fontweight='bold', color='white')

    # Status Text
    ax.text(0, -0.28, status, ha='center', va='center', 
            fontsize=15, fontweight='bold', color=status_color)

    # Title
    ax.text(0, 0.72, "Voltage Drop Compliance", ha='center', va='center',
            fontsize=17, fontweight='bold', color='white')

    # Scale labels (0%, 3%, 5%, 10%)
    for percent, label in [(0,'0%'), (3,'3%'), (5,'5%'), (10,'10%')]:
        angle = 180 - (percent * 18)
        rad = np.deg2rad(angle)
        x = 1.05 * np.cos(rad)
        y = 1.05 * np.sin(rad)
        ax.text(x, y, label, ha='center', va='center', fontsize=12, color='white', fontweight='bold')

    # Zone Labels
    ax.text(-0.75, -0.75, "GOOD", ha='center', fontsize=13, color='#2ecc71', fontweight='bold')
    ax.text(0, -0.88, "WARNING", ha='center', fontsize=13, color='#f1c40f', fontweight='bold')
    ax.text(0.75, -0.75, "FAIL", ha='center', fontsize=13, color='#e74c3c', fontweight='bold')

    ax.axis('equal')
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.05, 0.95)

    output_file = "voltage_drop_gauge.png"
    plt.savefig(output_file, dpi=350, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()

    return os.path.abspath(output_file)