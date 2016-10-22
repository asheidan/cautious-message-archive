from . import display_migrations

if __name__ == "__main__":
    # Stuff
    # Make sure that the table for schema migrations exist before
    # Applying magic
    display_migrations()
