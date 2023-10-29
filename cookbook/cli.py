from cookbook.app import app_builder

cli = app_builder.create_cli()

if __name__ == "__main__":
    cli()
