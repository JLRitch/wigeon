# standard imports

# external imports

# project imports
import commands


if commands.args.subcommand is None:
    commands.cli.print_help()
else:
    commands.args.func(commands.args)