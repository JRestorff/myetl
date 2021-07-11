import typer


app = typer.Typer()


@app.command()
def welcome():
    typer.echo("Welcome to myetl!")
