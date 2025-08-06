from fastapi import Request


def log(tag="MyApp", message="", request: Request = None):
    """
    Custom logging function to print messages with a tag.

    Args:
        tag (str): The tag to identify the log message.
        message (str): The message to log.
    """
    print(f"Logging: [{tag}] {message}")
    with open("log.txt", "a+") as log:
        log.write(f"{tag}: {message}\n")
        if request:
            log.write(f"\t{request.method} {request.url}\n")
            log.write(f"\tHeaders: {request.headers}\n")
            log.write(f"\tQuery Params: {request.query_params}\n")
