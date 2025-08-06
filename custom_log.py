def log(tag="", message=""):
    """
    Custom logging function to print messages with a tag.

    Args:
        tag (str): The tag to identify the log message.
        message (str): The message to log.
    """
    print(f"Logging: [{tag}] {message}")
    with open("log.txt", "w+") as log:
        log.write(f"{tag}: {message}\n")
