### Generating JWT

In the container, cd to visualapi/src and run this command:

`uv run cli.py jwt generate --sub youruser --exp 120`

The --sub parameter is required. In the example the --exp is expiration in minutes.
