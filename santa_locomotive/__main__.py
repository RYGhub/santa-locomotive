import typing as t
import click
import time
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
        click.secho(locomotive_on_rails(), bold=True, reverse=True)

    for name in names:
        try:
            game = find_next_stop(client=client, value=name)
        except steamfront.errors.AppNotFound:
            click.secho(f"error: game not found: {name}", err=True, bold=True, fg="bright_red")
        else:
            click.secho(game_on_rails(game))
        finally:
            time.sleep(1)


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
    return "NAME\t" \
           "APPID\t" \
           "PRICE\t" \
           "METASCORE\t" \
           "GENRES\t" \
           "PLATFORMS\t" \
           "DESCRIPTION\t" \
           "STORELINK"


def game_on_rails(game: app.App) -> str:
    """
    :param game: The :class:`steamfront.app.App` to format.
    :return: The formatted :class:`str`.
    """
    return f"{game.name}\t" \
           f"{game.appid}\t" \
           f"{money_on_rails(game.price_overview)}\t" \
           f"{reviews_on_rails(game.metacritic)}\t" \
           f"{subsection_on_rails(game.genres)}\t" \
           f"{platforms_on_rails(game.platforms)}\t" \
           f"{content_sanitizer(game.short_description)}\t" \
           f"https://store.steampowered.com/app/{game.appid}/"


def subsection_on_rails(subsection: list) -> str:
    return ";".join(subsection)


def platforms_on_rails(d: dict) -> str:
    return ";".join([key for key, value in d.items() if value])


def reviews_on_rails(d: dict) -> str:
    return f"{d['score']}"


def money_on_rails(d: t.Optional[dict]) -> str:
    if isinstance(d, dict):
        return d["final_formatted"]
    else:
        return "0.00€"


def content_sanitizer(content: str) -> str:
    return " ".join(content.split()).replace("<br />", " ")


if __name__ == "__main__":
    combustion_chamber()
