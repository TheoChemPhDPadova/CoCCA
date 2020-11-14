"""QM output reader"""
import sys
import argparse, QM_parser
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


def main(path):
    with open(path) as file:
        out = file.read()

    if 'Amsterdam Density Functional  (ADF)' in out or 'Amsterdam Modeling Suite (AMS)' in out:
        src = QM_parser.AMS(path)
        print('Software:\tADF/AMS {}'.format(src.version))
    elif 'O   R   C   A' in out:
        src = QM_parser.ORCA(path)
        print('Software:\tORCA {}'.format(src.version))
    elif ' Gaussian 16,' in out:
        src = QM_parser.G16(path)
        print('Software:\tGaussian 16 {}'.format(src.version))
    else:
        print('\nSorry, output file not supported!')
        sys.exit()

    x = np.arange(len(src.ene) - 1)
    fig = make_subplots(
        rows=3,
        cols=3,
        horizontal_spacing=0.05,
        vertical_spacing=0.10,
        subplot_titles=(
            "Energy / Ha", "Gradient MAX / Ha", "Displacement MAX / Å",
            "|Energy Change| / Ha", "Gradient RMS / Ha", "Displacement RMS / Å",
            "Eigenvectors"
        ))

    fig.add_trace(go.Scatter(x=x, y=src.ene, line=dict(color='black', width=1), marker=dict(color='black')), row=1, col=1)

    fig.add_trace(go.Scatter(x=x, y=src.grdmax, line=dict(color='darkorange', width=1), marker=dict(color='darkorange')), row=1, col=2)
    if src.grdmax[-1] < src.grdmaxlim:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.grdmaxlim,
            x1=x[-1],
            y1=src.grdmaxlim,
            line=dict(color='green', width=1),),
            row=1,
            col=2
        )
    else:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.grdmaxlim,
            x1=x[-1],
            y1=src.grdmaxlim,
            line=dict(color='red', width=1),),
            row=1,
            col=2
        )

    fig.add_trace(go.Scatter(x=x, y=src.stpmax, line=dict(color='royalblue', width=1), marker=dict(color='royalblue')), row=1, col=3)
    if src.stpmax[-1] < src.stpmaxlim:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.stpmaxlim,
            x1=x[-1],
            y1=src.stpmaxlim,
            line=dict(color='green', width=1),),
            row=1,
            col=3
        )
    else:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.stpmaxlim,
            x1=x[-1],
            y1=src.stpmaxlim,
            line=dict(color='red', width=1),),
            row=1,
            col=3
        )

    fig.add_trace(go.Scatter(x=x, y=[abs(i) for i in src.enechg[1:]], line=dict(color='black', width=1), marker=dict(color='black')), row=2, col=1)
    if src.enelim != '':
        if src.enechg[-1] < src.enelim:
            fig.add_shape(go.layout.Shape(
                type="line",
                x0=x[0],
                y0=src.enelim,
                x1=x[-1],
                y1=src.enelim,
                line=dict(color='green', width=1),),
                row=2,
                col=1
            )
        else:
            fig.add_shape(go.layout.Shape(
                type="line",
                x0=x[0],
                y0=src.enelim,
                x1=x[-1],
                y1=src.enelim,
                line=dict(color='red', width=1),),
                row=2,
                col=1
            )

    fig.add_trace(go.Scatter(x=x, y=src.grdrms, line=dict(color='darkorange', width=1), marker=dict(color='darkorange')), row=2, col=2)
    if src.grdrms[-1] < src.grdrmslim:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.grdrmslim,
            x1=x[-1],
            y1=src.grdrmslim,
            line=dict(color='green', width=1),),
            row=2,
            col=2
        )
    else:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.grdrmslim,
            x1=x[-1],
            y1=src.grdrmslim,
            line=dict(color='red', width=1),),
            row=2,
            col=2
        )

    fig.add_trace(go.Scatter(x=x, y=src.stprms, line=dict(color='royalblue', width=1), marker=dict(color='royalblue')), row=2, col=3)
    if src.stprms[-1] < src.stprmslim:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.stprmslim,
            x1=x[-1],
            y1=src.stprmslim,
            line=dict(color='green', width=1),),
            row=2,
            col=3
        )
    else:
        fig.add_shape(go.layout.Shape(
            type="line",
            x0=x[0],
            y0=src.stprmslim,
            x1=x[-1],
            y1=src.stprmslim,
            line=dict(color='red', width=1),),
            row=2,
            col=3
        )

    if src.eigen != []:
        for eig in src.eigen:
            fig.add_trace(go.Scatter(x=x, y=eig, line=dict(width=0.7)), row=3, col=1)

    fig.update_xaxes(range=[0, len(x) - 1], dtick=1)
    fig.update_layout(
        template="plotly_white",
        showlegend=False
    )
    fig.show()
    sys.exit()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-i", "--input", type=str, help="Path of the output file...")
    ARGS = PARSER.parse_args()
    main(ARGS.input)
