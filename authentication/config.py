TORTOISE_ORM = {
    "connections": {"default": "sqlite://comments.db"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  
            "default_connection": "default",
        }
    }
}