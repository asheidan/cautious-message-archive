import argparse


# http://stackoverflow.com/questions/20743587/how-to-debug-a-python-module-that-needs-to-be-executed-with-m#20881472
# Declare itself as package if needed
if __name__ == '__main__' and not __package__:
    import os
    import sys
    parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    sys.path.append(os.path.dirname(parent_dir))


def nop():
    pass


def parse_command_line():
    from backend.migrations import apply_migrations
    from backend.migrations import create_migration
    from backend.migrations import display_migrations

    parser = argparse.ArgumentParser()

    sub_parsers = parser.add_subparsers(title="Commands", metavar="<command>")

    list_parser = sub_parsers.add_parser(
        "list",
        help="List the available migrations"
    )
    list_parser.set_defaults(func=display_migrations)

    apply_parser = sub_parsers.add_parser(
        "apply",
        help="Try to apply all migrations not already applied"
    )
    apply_parser.set_defaults(func=apply_migrations)

    create_subparser = sub_parsers.add_parser(
        "create",
        help="Create new migration"
    )
    create_subparser.set_defaults(func=create_migration)
    create_subparser.add_argument("migration_name", metavar="NAME", type=str,
                                  help=("The name of the migration."
                                        " (Will be used for filename)"))

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    # Stuff

    args = parse_command_line()

    # Make sure that the table for schema migrations exist before
    # Applying magic
    args.func(args)
