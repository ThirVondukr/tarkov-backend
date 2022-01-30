from pathlib import Path

import uvicorn

import utils


def main() -> None:
    certs_directory = Path("resources/certs")
    certs_directory.mkdir(exist_ok=True)
    utils.generate_certificates(certs_directory)

    uvicorn.run(
        "app:create_app",
        port=443,
        factory=True,
        use_colors=False,
        ssl_keyfile="resources/certs/key.pem",
        ssl_certfile="resources/certs/certificate.pem",
        ssl_keyfile_password=" ",
    )


if __name__ == "__main__":
    main()
