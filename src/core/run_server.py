from .app import create_app
import uvicorn
from core.configuration import configuration


def bootstrap():
    app = create_app()
    uvicorn.run(
        f"{__name__}:{create_app.__name__}",
        port=configuration.port,
        reload=configuration.is_debug,
        host="0.0.0.0",
        factory=True,
        server_header=True,
    )
