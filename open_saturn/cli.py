import click
from open_saturn.helper import host

@click.command()
def openwebstart():
    from open_saturn.wsgi import app
    app.run(host=host(), debug=False)
