import media2ascii.media as media
import typer
import logging
import sys
import os

# Log config
LOG_FORMAT = "%(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger()

# CLI app instancing
app = typer.Typer()


# main execution
@app.command()
def generate(filename: str):
    input_path = os.path.join(os.getcwd(), filename.lower())
    print(input_path)
    exists = os.path.exists(input_path)
    if not exists:
        log.info("ERROR: File does not exists or is not readable.")
        return

    valid = media.validate(input_path)
    if valid['img']:
        media.get_ascii_from_image(input_path)
    elif valid['video']:
        media.get_ascii_from_media(input_path)
    else:
        log.info("ERROR: File type not supported.")


# CLI app loop
if __name__ == '__main__':
    app()
