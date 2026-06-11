import matplotlib.pyplot as plt
import os
from gauge_generator import create_gauge

def generate_chart(results):
    vd_percent = results.get('vd_percent', 0.0)
    return create_gauge(vd_percent)
    
    fig, ax = plt.subplots(figsize=(10, 3.2))
    
    # Zones
    ax.barh(0, 3, left=0, color='#2ecc71', height=0.65)   # Green 0-3%
    ax.barh(0, 2, left=3, color='#f1c40f', height=0.65)   # Yellow 3-5%
    ax.barh(0, 5, left=5, color='#e74c3c', height=0.65)   # Red 5-10%
    
    # Pointer
    pointer_x = min(vd_percent, 10)
    ax.plot([pointer_x, pointer_x], [-0.4, 0.95], color='white', linewidth=7, zorder=5)
    ax.plot([pointer_x, pointer_x], [-0.4, 0.95], color='#00ccff', linewidth=4, zorder=6)
    
    # Value on top
    ax.text(pointer_x, 1.25, f'{vd_percent:.2f}%', ha='center', va='bottom',
            fontsize=13, fontweight='bold', color='#00ccff')
    
    # Status
    if vd_percent <= 3:
        status = "GOOD"
        color = "#2ecc71"
    elif vd_percent <= 5:
        status = "WARNING"
        color = "#f1c40f"
    else:
        status = "FAIL"
        color = "#e74c3c"
    
    ax.text(5, -1.1, status, ha='center', fontsize=15, fontweight='bold', color=color)
    
    # Scale labels
    for x, label in [(0,'0%'), (3,'3%'), (5,'5%'), (10,'10%')]:
        ax.text(x, -0.25, label, ha='center', fontsize=11, color='white')
    
    # Zone labels
    ax.text(1.5, -0.85, 'GOOD', ha='center', fontsize=11, color='white', fontweight='bold')
    ax.text(4, -0.85, 'WARNING', ha='center', fontsize=11, color='white', fontweight='bold')
    ax.text(7.5, -0.85, 'FAIL', ha='center', fontsize=11, color='white', fontweight='bold')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.4, 1.6)
    ax.axis('off')
    
    # Background
    ax.set_facecolor('#111111')
    fig.patch.set_facecolor('#111111')
    
    chart_file = "voltage_drop_gauge.png"
    plt.savefig(chart_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    return os.path.abspath(chart_file)