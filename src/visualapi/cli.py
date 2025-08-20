"""Cli tool for visualapi.

Allows users to create JWT tokens for accessing the visualapi service.
Blacklists tokens and provides a simple interface to manage these tokens.
"""

import datetime
import uuid

import api
import click
from auth import blacklist as jwt_blacklist
from auth.api import AUDIENCE
from auth.jwt import decode_jwt, encode_jwt
from config import settings

ISSUER = "visualapi-admin-cli"


# Defined endpoint access segments
SEGMENTS = api.SCOPES


@click.group()
def cli():
    pass


@cli.group()
def blacklist():
    """Manage JWT blacklist."""
    pass


@cli.group()
def jwt():
    """JWT operations."""
    pass


@jwt.command("decode")
@click.argument("token")
def decode_jwt_cmd(token):
    """Decode a JWT and display its payload."""
    try:
        payload = decode_jwt(token, audience=AUDIENCE)
        click.secho("Decoded JWT payload:", fg="green", bold=True)
        for key, value in payload.items():
            key_str = click.style(f"{key}", fg="cyan", bold=True)
            value_str = click.style(f"{value}", fg="yellow")
            click.echo(f"  {key_str}: {value_str}")
    except Exception as e:
        click.secho(f"Failed to decode JWT: {e}", fg="red", err=True)
        raise click.Abort()


@jwt.command("generate")
@click.option(
    "--sub",
    required=True,
    help="Subject of the token. Usually the user ID or username.",
)
@click.option(
    "--exp",
    type=int,
    default=60,
    help="Token expiration in minutes (default: 60 minutes)",
)
@click.option(
    "--claim",
    multiple=True,
    help="Additional custom claim(s) in key=value format. Can be repeated.",
)
@click.option(
    "--allow",
    multiple=True,
    type=click.Choice(SEGMENTS),
    help=f"List of allowed endpoint segments. Repeat for multiple (choices: {', '.join(SEGMENTS)})",
)
def generate_jwt(sub, exp, claim, allow):
    """Generate a JWT with the specified subject, expiration, claims, and allowed segments."""
    if not settings.API_JWT_SECRET:
        click.echo("Error: SECRET_KEY environment variable not set.", err=True)
        raise click.Abort()

    payload = {
        "iss": ISSUER,
        "sub": sub,
        "aud": AUDIENCE,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=exp),
        "jti": str(uuid.uuid4()),
    }

    if allow:
        payload["scopes"] = list(allow)

    for c in claim:
        if "=" not in c:
            click.echo(f"Invalid claim format: {c}. Use key=value.", err=True)
            raise click.Abort()
        key, value = c.split("=", 1)
        payload[key.strip()] = value.strip()

    token = encode_jwt(payload, settings.API_JWT_SECRET)
    click.secho("\nGenerated JWT:", fg="green", bold=True)
    click.secho(token, fg="yellow", bold=True)
    click.secho("\nJWT Payload:", fg="blue", bold=True)

    for key, value in payload.items():
        key_str = click.style(f"{key}", fg="cyan", bold=True)
        value_str = click.style(f"{value}", fg="magenta")
        click.echo(f"  {key_str}: {value_str}")

    click.echo("\n")


@blacklist.command("add")
@click.argument("token")
def blacklist_add(token):
    """Add a JWT's jti to the blacklist."""
    try:
        payload = decode_jwt(settings.API_JWT_SECRET, token, audience=AUDIENCE)
        jti = payload.get("jti")
        if not jti:
            click.secho("JWT does not contain a 'jti' claim.", fg="red", err=True)
            raise click.Abort()
        jwt_blacklist.blacklist_token(jti)
        click.secho(f"jti '{jti}' has been blacklisted.", fg="green")
    except Exception as e:
        click.secho(f"Failed to blacklist token: {e}", fg="red", err=True)
        raise click.Abort()


@blacklist.command("check")
@click.argument("token")
def blacklist_check(token):
    """Check if a JWT's jti is blacklisted."""
    try:
        payload = decode_jwt(settings.API_JWT_SECRET, token, audience=AUDIENCE)
        jti = payload.get("jti")
        if not jti:
            click.secho("JWT does not contain a 'jti' claim.", fg="red", err=True)
            raise click.Abort()
        if jwt_blacklist.is_token_blacklisted(jti):
            click.secho(f"jti '{jti}' is blacklisted.", fg="red")
        else:
            click.secho(f"jti '{jti}' is NOT blacklisted.", fg="green")
    except Exception as e:
        click.secho(f"Failed to check blacklist: {e}", fg="red", err=True)
        raise click.Abort()


cli.add_command(blacklist)


if __name__ == "__main__":
    cli()
