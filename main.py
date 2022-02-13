import os

import uvicorn

import paths
import utils


def main() -> None:
    paths.certificates.mkdir(exist_ok=True)
    utils.generate_certificates(paths.certificates)
    uvicorn.run(
        "app:create_app",
        port=443,
        reload=bool(os.environ.get("RELOAD")),
        factory=True,
        use_colors=False,
        ssl_keyfile="resources/certs/key.pem",
        ssl_certfile="resources/certs/certificate.pem",
        ssl_keyfile_password=" ",
    )


if __name__ == "__main__":
    main()
