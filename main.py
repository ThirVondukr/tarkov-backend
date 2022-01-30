import uvicorn


def main() -> None:
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
