import click
import steamfront
import steamfront.errors
from steamfront import app as app


@click.command()
@click.option(
    '--include-header/--exclude-header',
    "include_header",
    default=True,
    help="Adds an header detailing the column contents.",
)
@click.argument(
    "names",
    nargs=-1,
)
def combustion_chamber(include_header, names):
    client = steamfront.Client()

    if include_header:
        click.secho(locomotive_on_rails(), bold=True, underline=True, bg="bright_white", fg="black")

    for name in names:
        try:
            game = find_next_stop(client=client, value=name)
            game_on_rails(game)
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


def locomotive_on_rails() -> str:
    """
    Get the results header.
    """
    return "AppName\tAppID\tGenres\tFeatures\tBannerImageURL\tSummary\tDescription"


def game_on_rails(game: app.App) -> str:
    click.echo("{}\t{}\t{}\t{}\t{}\t{}\t\n".format(game.appid, subsection_on_rails(game.genres),
                                                   subsection_on_rails(game.categories), game.header_image,
                                                   content_sanitizer(game.short_description),
                                                   content_sanitizer(game.detailed_description)
                                                   )
               )


def subsection_on_rails(subsection: list) -> str:
    return ";".join(subsection)


def content_sanitizer(content: str) -> str:
    return " ".join(content.split())


if __name__ == "__main__":
    combustion_chamber()
