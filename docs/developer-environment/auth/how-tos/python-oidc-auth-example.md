# OIDC Authentication Example

Example for how to handle basic OIDC authentication.

Note that this project does not use framework specific libraries for actually handling the authentication flow, but instead implements it through the `Auth` class described in the linked repository.

To clone the repository containing the code for this tutorial, run:

```shell
git clone https://gitlab.diamond.ac.uk/sscc-docs/python-oidc-auth-example
```

For more information, read the comments present in source files.

!!! note

    Although the described routes are mostly relevant to FastAPI, these can be modified to match Django or Flask blueprints

## Before you start

You must have [registered your application with CAS.](./registering-a-service-with-cas.md)

## Configuration

Set the environment variables `CLIENT_ID` and `CLIENT_SECRET` to the values you received in the previous step, and also make sure that the endpoint described in `config.json` points to a valid discovery endpoint (a JSON object containing details about the OIDC implementation you want to interact with). The default file points to Diamond's CAS.

!!! note

    Client secrets and IDs must never be included in public clients (like webpages), do not use credentials meant for other applications whenever applicable

If your `config.json` file is not in the same folder you're running the example from, change the environment variable `CONFIG_PATH` to point to the location of your file. It is relative to the folder you run uvicorn from.

## Running

1. Install the package with `pip install .` or `pip install -e .`
2. Run `uvicorn` with `uvicorn auth_example.main:app --reload --port 8000`

If you see something when opening `http://localhost:8000/docs` in your browser, you are good to go!

If the service ID (the accepted pattern for your redirect URI) you have registered for your application does not match `localhost` (and it most likely won't), you can map a given address (hostname) to localhost (127.0.0.1) or use `local-oidc-test.diamond.ac.uk` as an alias for localhost.
