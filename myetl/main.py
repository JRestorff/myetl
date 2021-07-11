from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
import typer


app = typer.Typer()


@app.command()
def execute():
    engine = create_engine("sqlite://")
    root_folder = Path.cwd()

    data_folder = root_folder / "data"
    for file in data_folder.iterdir():
        name = file.stem
        pd.read_csv(file).to_sql(name, engine)

    transform_folder = root_folder / "transforms"
    out_folder = root_folder / "output"
    if not out_folder.exists():
        out_folder.mkdir()
    with engine.connect() as con:
        for file in transform_folder.iterdir():
            name = file.stem
            with open(file, "r") as f:
                query = f.read()
                statement = f"create table {name} as {query}"
                con.execute(statement)

            out_file = out_folder / f"{name}.csv"
            pd.read_sql_table(name, engine).to_csv(out_file)

    engine.dispose()
