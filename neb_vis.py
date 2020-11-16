"""Neb Visualizer"""
import sys, os
import utils
import plotly.graph_objects as go


def main(path):
    utils.TITLE("NEB Visualizer (ORCA)")
    fig = go.Figure()

    with open(path) as file:
        lines = file.readlines()

    idx_pts = []
    idx_int = []

    for idx, val in enumerate(lines):
        if "Images:" in val:
            idx_pts.append(idx + 1)
        elif "Interp.:" in val:
            idx_int.append(idx + 1)

    pts_n = idx_int[0] - 6

    if len(idx_pts) != 1:
        int_n = idx_pts[1] - idx_int[0] - 3
    else:
        int_n = len(lines) - idx_int[0]

    for i in idx_pts:
        if i == idx_pts[0]:
            x = [float(lines[j].split()[0]) for j in range(i, i + pts_n)]
            y = [float(lines[j].split()[1]) * utils.ha2kcal for j in range(i, i + pts_n)]
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='markers', marker=dict(color='darkorange')))
        elif i == idx_pts[-1]:
            x = [float(lines[j].split()[0]) for j in range(i, i + pts_n)]
            y = [float(lines[j].split()[1]) * utils.ha2kcal for j in range(i, i + pts_n)]
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='markers', marker=dict(color='cornflowerblue')))
        else:
            x = [float(lines[j].split()[0]) for j in range(i, i + pts_n)]
            y = [float(lines[j].split()[1]) * utils.ha2kcal for j in range(i, i + pts_n)]
            fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='markers', marker=dict(color='gainsboro')))

    for i in idx_int:
        if i == idx_int[0]:
            x = [float(lines[j].split()[0]) for j in range(i, i + int_n)]
            y = [float(lines[j].split()[1]) * utils.ha2kcal for j in range(i, i + int_n)]
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='lines', line=dict(color='darkorange')))
        elif i == idx_int[-1]:
            x = [float(lines[j].split()[0]) for j in range(i, i + int_n)]
            y = [float(lines[j].split()[1]) * utils.ha2kcal for j in range(i, i + int_n)]
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='lines', line=dict(color='cornflowerblue')))
        else:
            x = [float(lines[j].split()[0]) for j in range(i, i + int_n)]
            y = [float(lines[j].split()[1]) * utils.ha2kcal for j in range(i, i + int_n)]
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='lines', line=dict(color='gainsboro')))

    fig.update_layout(
        title="ORCA Nudged Elastic Band ",
        xaxis_title="Iteration",
        yaxis_title="E / kcal mol<sup>-1</sup>",
        template="plotly_white",
        showlegend=False
    )
    fig.show()
    utils.NT()


if __name__ == "__main__":
    try:
        path = input("Enter .interp file path...\t\t")
        main(path)
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
