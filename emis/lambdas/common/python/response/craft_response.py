def craft_response(status_code, body=None):
    headers = {
        'Content-Type': 'application/json',
    }
    response = {
        'statusCode': status_code,
        'headers': headers,
        'body': body,
    }

    return response
