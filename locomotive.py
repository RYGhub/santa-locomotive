import click
import steamfront
from steamfront import app as app


@click.command()
@click.option('--output_format', default="tabs", help="The output format. By default, its Tab Separated Values. \n" +
                                                      "For now, only 'tabs' is supported.")
@click.option('--include_header', default=False, help="Enables the inclusion of the header as part of the output." +
                                                      "\nIgnored if output format is not tabs.")
@click.argument("names", nargs=-1)
def combustion_chamber(include_header, output_format, names):
    client = steamfront.Client()
    if include_header and output_format != "json":
        click.echo("APPID\tGENRES\tCATEGORIES\tBANNER_URL\tSHORT_DESC\tLONG_DESC\t\n")
    for name in names:
        try:
            game = client.getApp(name=name)
            game_on_rails(game, output_format)
        except steamfront.client._AppNotFound:
            click.echo(err=True, message="Game not found: {}".format(name))


def game_on_rails(game: app.App, output_format):
    if output_format == "tabs":
        click.echo("{}\t{}\t{}\t{}\t{}\t{}\t\n".format(game.appid, subsection_on_rails(game.genres),
                                                       subsection_on_rails(game.categories), game.header_image,
                                                       content_sanitizer(game.short_description),
                                                       content_sanitizer(game.detailed_description)
                                                       )
                   )
    else:
        raise NotImplementedError


def subsection_on_rails(subsection: list) -> str:
    return ";".join(subsection)


def content_sanitizer(content: str) -> str:
    return " ".join(content.split())


if __name__ == "__main__":
    combustion_chamber()
