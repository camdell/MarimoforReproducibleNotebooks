import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium")


@app.cell
def _():
    from polars import read_csv, col

    df = read_csv('raw_training_study.csv')
    return col, df


@app.cell
def _(mo):
    mo.md(r"""
    # Interactive data filtration

    select the number of standard deviations that you want to filter +/- the mean from the 'score' column
    """)
    return


@app.cell
def _():
    import marimo as mo

    NSTD = mo.ui.slider(start=1, stop=4)
    NSTD
    return NSTD, mo


@app.cell(hide_code=True)
def _(NSTD, mo):
    mo.md(rf"""
    You will filter the score column by its mean +/- {NSTD.value}
    """)
    return


@app.cell
def _(NSTD):
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--nstd', default=NSTD.value, type=int)
    args = parser.parse_args()

    return (args,)


@app.cell
def _(args, col, df):
    clean_df = (
        df.filter(
            col('hours', 'score').is_not_null(),
            col('score').is_between(0, 100),
            ((col('hours') > (col('hours').mean() - (col('hours').std() * args.nstd)))
             & (col('hours') < (col('hours').mean() + (col('hours').std() * args.nstd))))
        )
        .with_columns(
            col('score') / 100
        )
    )

    print(clean_df)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
