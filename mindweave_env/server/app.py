# mindweave_env/server/app.py

from openenv.core.env_server.http_server import create_app

# .clean absolute imports
from mindweave_env.models import MindweaveAction, MindweaveObservation
from mindweave_env.server.environment2 import MindweaveEnvironment


# =========================
# . CREATE APP
# =========================
app = create_app(
    MindweaveEnvironment,
    MindweaveAction,
    MindweaveObservation,
    env_name="mindweave_env",
    max_concurrent_envs=1,
)


# =========================
# . OPTIONAL LOCAL RUN
# =========================
# inside mindweave_env/server/app.py
import uvicorn

def main():
    uvicorn.run("mindweave_env.server.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()