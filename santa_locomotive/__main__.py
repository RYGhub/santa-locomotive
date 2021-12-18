import click
import steamfront
import steamfront.errors
from steamfront import app as app


@click.command()
@click.option(
    '--include-header/--exclude-header',
    "include_header",
    default=False,
    help="Adds an header detailing the column contents.\nIgnored if output format is not tabs.",
)
@click.option(
    '--output-format',
    "output_format",
    default="tabs",
    help="The format the program should output data as. Available values: 'tabs'",
)
@click.argument(
    "names",
    nargs=-1,
)
def combustion_chamber(include_header, output_format, names):
    client = steamfront.Client()
    if include_header and output_format == "tabs":
        click.echo("APPID\tGENRES\tCATEGORIES\tBANNER_URL\tSHORT_DESC\tLONG_DESC\t\n")
    for name in names:
        try:
            game = find_next_stop(client=client, value=name)
            game_on_rails(game, output_format)
        except steamfront.client._AppNotFound:
            click.echo(err=True, message="Game not found: {}".format(name))


def find_next_stop(client: steamfront.Client, value: str) -> steamfront.app.App:
    """
    :param client: The :class:`steamfront.Client` to use.
    :param value: The :class:`str` to search for, either a game name or an AppID.
    :return: The ~~next stop~~ found :class:`steamfront.app.App`.
    :raises steamfront.errors.AppNotFound: If no app was found, both by AppID and by name.
    """
    try:
        return client.getApp(appid=value)
    except (ValueError, TypeError, steamfront.errors.AppNotFound):
        return client.getApp(name=value)


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
