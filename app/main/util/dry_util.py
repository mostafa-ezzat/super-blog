def create_response(status, message, extra=None):
    response = {
        'status': status,
        'message': message,
    }

    # exitra is a dictionary if it exist we will
    # loop it and add it to the response
    if extra and isinstance(extra, dict):
        for key in extra:
            response[key] = extra[key]

    return response
