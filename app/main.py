#!/usr/bin/env python
from app.config.application import create_app

application = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(application, host="127.0.0.1", port=8000)
