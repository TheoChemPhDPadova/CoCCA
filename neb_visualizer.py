"""Neb Visualizer"""
import matplotlib.pyplot as plt

print("""
================================================
            NEB Visualizer (ORCA)
================================================\n
""")

with open("1.interp") as file:
    lines = file.readlines()

HAKC = 627.509
idx_pts = []
idx_int = []

for idx, val in enumerate(lines):
    if "Images:" in val:
        idx_pts.append(idx + 1)
    elif "Interp.:" in val:
        idx_int.append(idx + 1)

pts_n = idx_int[0] - 6
int_n = idx_pts[1] - idx_int[0] - 3

for i in idx_pts:
    if i == idx_pts[0]:
        x = [float(lines[j].split()[0]) for j in range(i, i+pts_n)]
        y = [float(lines[j].split()[2])*HAKC for j in range(i, i+pts_n)]
        plt.scatter(x, y, s=15, c="orange")
    elif i == idx_pts[-1]:
        x = [float(lines[j].split()[0]) for j in range(i, i+pts_n)]
        y = [float(lines[j].split()[2])*HAKC for j in range(i, i+pts_n)]
        plt.scatter(x, y, s=15, c="cornflowerblue", zorder=10)
    else:
        x = [float(lines[j].split()[0]) for j in range(i, i+pts_n)]
        y = [float(lines[j].split()[2])*HAKC for j in range(i, i+pts_n)]
        plt.scatter(x, y, s=7, c="gainsboro")

for i in idx_int:
    if i == idx_int[0]:
        x = [float(lines[j].split()[0]) for j in range(i, i+int_n)]
        y = [float(lines[j].split()[2])*HAKC for j in range(i, i+int_n)]
        plt.plot(x, y, c="orange")
    elif i == idx_int[-1]:
        x = [float(lines[j].split()[0]) for j in range(i, i+int_n)]
        y = [float(lines[j].split()[2])*HAKC for j in range(i, i+int_n)]
        plt.plot(x, y, c="cornflowerblue", zorder=10)
    else:
        x = [float(lines[j].split()[0]) for j in range(i, i+int_n)]
        y = [float(lines[j].split()[2])*HAKC for j in range(i, i+int_n)]
        plt.plot(x, y, c="gainsboro")

plt.xlim(0, 1)
plt.show()
