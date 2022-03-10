from schemas import schema


errors = {
    400: {
        "model": schema.Message,
        "description": "Bad Request"
    },
    401: {
        "model": schema.Message,
        "description": "Unauthorized"
    },
    403: {
        "model": schema.Message,
        "description": "Forbidden"
    },
    404: {
        "model": schema.Message,
        "description": "Not Found"
    },
    405: {
        "model": schema.Message,
        "description": "Method Not Allowed"
    }
}