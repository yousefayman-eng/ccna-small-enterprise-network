#!/usr/bin/env python3
"""Render the Small Enterprise Network topology diagram (PNG)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Ellipse

VLAN_COLORS = {
    10: "#2563eb", 20: "#0d9488", 30: "#ea580c", 40: "#7c3aed",
    50: "#16a34a", 99: "#475569", 999: "#94a3b8",
}
ROUTER = "#1e40af"; SWITCH = "#0e7490"; END = "#ffffff"; CLOUD = "#e2e8f0"
INK = "#0f172a"; LINK = "#334155"

fig, ax = plt.subplots(figsize=(16, 10), dpi=200)
ax.set_xlim(0, 160); ax.set_ylim(0, 100); ax.axis("off")
fig.patch.set_facecolor("white")

def link(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=LINK, lw=2.2, zorder=1, solid_capstyle="round")

def label(x, y, text, size=8.5, color=INK, weight="normal", ha="center", bg=True):
    bbox = dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.92) if bg else None
    ax.text(x, y, text, size=size, color=color, weight=weight, ha=ha, va="center",
            zorder=6, bbox=bbox)

def router(cx, cy, name):
    c = Circle((cx, cy), 5.6, fc=ROUTER, ec="#172554", lw=2, zorder=4)
    ax.add_patch(c)
    ax.plot([cx-3.2, cx+3.2], [cy+1.2, cy+1.2], color="white", lw=1.1, zorder=5)
    ax.plot([cx-3.2, cx+3.2], [cy-1.2, cy-1.2], color="white", lw=1.1, zorder=5)
    for dx, dy in ((0, 2.6), (-2.8, -2.4), (2.8, -2.4)):
        ax.annotate("", xy=(cx+dx*1.9, cy+dy*1.9), xytext=(cx, cy),
                    arrowprops=dict(arrowstyle="-|>", color="white", lw=1.3), zorder=5)
    label(cx, cy-8.4, name, size=10.5, weight="bold")
    label(cx, cy-11.2, "2911", size=8, color="#475569")

def switch(cx, cy, name, w=23, h=8.6):
    b = FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="round,pad=0.4,rounding_size=1.6",
                       fc=SWITCH, ec="#155e75", lw=2, zorder=4)
    ax.add_patch(b)
    ax.annotate("", xy=(cx-3, cy+1.6), xytext=(cx-9, cy+1.6),
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4), zorder=5)
    ax.annotate("", xy=(cx+3, cy-1.6), xytext=(cx+9, cy-1.6),
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4), zorder=5)
    ax.annotate("", xy=(cx+9, cy+1.6), xytext=(cx+3, cy+1.6),
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4), zorder=5)
    ax.annotate("", xy=(cx-9, cy-1.6), xytext=(cx-3, cy-1.6),
                arrowprops=dict(arrowstyle="-|>", color="white", lw=1.4), zorder=5)
    label(cx, cy-7.4, name, size=10, weight="bold")

def pc(cx, cy, name, vlan, note):
    w, h = 15.2, 8.2
    b = FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle="round,pad=0.3,rounding_size=1.2",
                       fc=END, ec=VLAN_COLORS[vlan], lw=2.4, zorder=4)
    ax.add_patch(b)
    ax.text(cx, cy+0.8, name, size=8.2, weight="bold", ha="center", va="center", zorder=5, color=INK)
    ax.text(cx, cy-2.2, note, size=6.6, ha="center", va="center", zorder=5, color="#475569", linespacing=1.25)
    ax.add_patch(Circle((cx-w/2+2.0, cy+h/2-1.8), 1.0, fc=VLAN_COLORS[vlan], ec="none", zorder=5))
    ax.text(cx-w/2+3.5, cy+h/2-1.8, f"V{vlan}", size=6.6, weight="bold", color=VLAN_COLORS[vlan],
            ha="left", va="center", zorder=5)

# ---------------- Title ----------------
ax.text(80, 98.4, "Small Enterprise Network Design", size=19, weight="bold", ha="center", color=INK)
ax.text(80, 94.9, "HQ + Branch  ·  VLANs  ·  Inter-VLAN Routing  ·  OSPF  ·  DHCP  ·  NAT/PAT  ·  ACLs",
        size=10.5, ha="center", color="#475569")

# ---------------- ISP cloud ----------------
ax.add_patch(Ellipse((80, 85.5), 44, 13, fc=CLOUD, ec="#64748b", lw=2, zorder=3))
ax.text(80, 87.9, "ISP", size=13, weight="bold", ha="center", color=INK, zorder=5)
ax.text(80, 83.5, "Loopback0: 8.8.8.8/32  (internet test host)", size=8.2, ha="center", color="#475569", zorder=5)

# ---------------- Routers ----------------
router(54, 68, "R1-HQ")
router(114, 68, "R2-BRANCH")

# ISP <-> R1
link(63, 80.5, 56.5, 73.6)
label(46.5, 79.2, "203.0.113.0/30", size=8.8, weight="bold", color="#b91c1c")
label(61.6, 81.6, "G0/0  .1", size=7.4, color="#475569", ha="left")
label(52.4, 75.4, "G0/2  .2", size=7.4, color="#475569", ha="right")

# R1 <-> R2
link(59.9, 68, 108.1, 68)
label(84, 70.6, "10.255.12.0/30  ·  OSPF area 0", size=8.8, weight="bold", color="#b91c1c")
label(64, 65.4, "G0/1  .1", size=7.4, color="#475569", ha="left")
label(104, 65.4, "G0/1  .2", size=7.4, color="#475569", ha="right")

# ---------------- Switches ----------------
switch(30, 44, "SW1-HQ  (2960)")
switch(76, 44, "SW2-HQ  (2960)")
switch(124, 44, "SW3-BRANCH  (2960)")

# Trunks
link(48.5, 63.5, 34.5, 48.7)
label(28, 56.5, "Trunk 802.1Q\nG0/0 ↔ G0/1\nVLANs 10,20,30,40,99\nnative 999", size=7.2, color="#475569")
link(41.9, 44, 64.1, 44)
label(53, 47.4, "Trunk 802.1Q\nG0/2 ↔ G0/1\nVLANs 10,20,30,40,99\nnative 999", size=7.2, color="#475569")
link(118.5, 63.5, 122.5, 48.7)
label(135, 56.5, "Trunk 802.1Q\nG0/0 ↔ G0/1\nVLANs 50,99\nnative 999", size=7.2, color="#475569")

# ---------------- Endpoints ----------------
pc(12, 25, "PC-Staff-1", 10, "DHCP\n192.168.10.0/24")
pc(31, 25, "PC-IT-1", 20, "DHCP\n192.168.20.0/24")
pc(50, 25, "SRV1", 40, "static 192.168.40.10\nDNS + Web")
pc(67, 25, "PC-Guest-1", 30, "DHCP · 192.168.30.0/24\ninternet only (ACL 100)")
pc(88, 25, "PC-Staff-2", 10, "DHCP\n192.168.10.0/24")
pc(124, 25, "PC-Branch-1", 50, "DHCP\n172.16.50.0/24")

link(12, 39.6, 12, 29.2); label(9.6, 34.5, "F0/1", size=7, color="#475569", ha="right")
link(31, 39.6, 31, 29.2); label(28.6, 34.5, "F0/2", size=7, color="#475569", ha="right")
link(50, 39.6, 50, 29.2); label(47.6, 34.5, "F0/3", size=7, color="#475569", ha="right")
link(67, 39.6, 67, 29.2); label(64.6, 34.5, "F0/1", size=7, color="#475569", ha="right")
link(88, 39.6, 88, 29.2); label(85.6, 34.5, "F0/2", size=7, color="#475569", ha="right")
link(124, 39.6, 124, 29.2); label(121.6, 34.5, "F0/1", size=7, color="#475569", ha="right")

# ---------------- VLAN legend ----------------
lx, ly = 7, 15.5
b = FancyBboxPatch((lx-3.4, ly-11.0), 64, 14.8, boxstyle="round,pad=0.5,rounding_size=1.6",
                   fc="#f8fafc", ec="#cbd5e1", lw=1.4, zorder=3)
ax.add_patch(b)
ax.text(lx, ly+2.0, "VLANs", size=9.5, weight="bold", color=INK, zorder=5)
rows = [
    (10, "STAFF - 192.168.10.0/24 (HQ)"), (20, "IT - 192.168.20.0/24 (HQ)"),
    (30, "GUEST - 192.168.30.0/24 (HQ, isolated by ACL 100)"),
    (40, "SERVERS - 192.168.40.0/24 (HQ)"), (50, "BRANCH-USERS - 172.16.50.0/24"),
    (99, "MANAGEMENT - 192.168.99.0/24 (HQ), 172.16.99.0/24 (Branch)"),
    (999, "PARKING / native - no hosts, unused ports"),
]
for i, (v, txt) in enumerate(rows):
    yy = ly - 0.4 - i*1.55
    ax.add_patch(Circle((lx+1, yy), 0.85, fc=VLAN_COLORS[v], ec="none", zorder=5))
    ax.text(lx+2.6, yy, f"VLAN {v}  {txt}", size=7.6, color=INK, ha="left", va="center", zorder=5)

# ---------------- Notes box ----------------
nx, ny = 78, 15.5
b = FancyBboxPatch((nx-3.4, ny-11.0), 86, 14.8, boxstyle="round,pad=0.5,rounding_size=1.6",
                   fc="#f8fafc", ec="#cbd5e1", lw=1.4, zorder=3)
ax.add_patch(b)
ax.text(nx, ny+2.0, "Notes", size=9.5, weight="bold", color=INK, zorder=5)
notes = [
    "Management SVIs (VLAN 99, static): SW1-HQ 192.168.99.11,",
    "    SW2-HQ 192.168.99.12, SW3-BRANCH 172.16.99.11",
    "SSH v2 on all routers/switches; VTY ACL 23 = management only",
    "NAT overload (PAT) on R1-HQ G0/2 (public IP 203.0.113.2)",
    "R2-BRANCH gets its default route from OSPF (O*E2 via R1-HQ)",
    "HQ DHCP on R1-HQ (VLANs 10/20/30); branch DHCP on R2-BRANCH",
    "ACL 110: only HTTP/HTTPS/DNS/ping may reach SRV1",
]
for i, txt in enumerate(notes):
    ax.text(nx, ny - 0.4 - i*1.55, txt, size=7.6, color=INK, ha="left", va="center", zorder=5)

plt.savefig("/downloads/ccna-small-enterprise-network/topology/topology.png",
            bbox_inches="tight", facecolor="white")
print("saved")
