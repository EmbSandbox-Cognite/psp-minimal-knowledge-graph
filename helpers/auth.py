"""CDF authentication helpers.

Supports two OAuth flows selectable via the AUTH_FLOW env var:

    interactive          Browser-based login (default, for notebook users).
    client_credentials   Service principal login (for CI / headless scripts).
"""

from __future__ import annotations

import os
from pathlib import Path

from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthClientCredentials, OAuthInteractive
from dotenv import load_dotenv

VALID_AUTH_FLOWS = ("interactive", "client_credentials")


def _get_credentials(
    cluster: str, tenant_id: str, client_id: str, auth_flow: str
) -> OAuthClientCredentials | OAuthInteractive:
    if auth_flow == "client_credentials":
        return OAuthClientCredentials.default_for_entra_id(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=os.environ["CLIENT_SECRET"],
            cdf_cluster=cluster,
        )
    return OAuthInteractive.default_for_entra_id(
        tenant_id=tenant_id,
        client_id=client_id,
        cdf_cluster=cluster,
    )

def get_client(
    client_name: str = "coffee-roastery-demo", api_subversion: str | None = None
) -> CogniteClient:
    """Build a CogniteClient from environment variables.

    Required env vars (loaded from a .env file at the repo root):
        CDF_CLUSTER, CDF_PROJECT, CLIENT_ID, TENANT_ID

    Optional:
        AUTH_FLOW       "interactive" (default) or "client_credentials"
        CLIENT_SECRET   Required when AUTH_FLOW=client_credentials
    """
    repo_root = Path(__file__).resolve().parent.parent
    load_dotenv(repo_root / ".env")

    cluster = os.environ["CDF_CLUSTER"]
    project = os.environ["CDF_PROJECT"]
    client_id = os.environ["CLIENT_ID"]
    tenant_id = os.environ["TENANT_ID"]

    auth_flow = os.environ.get("AUTH_FLOW", "interactive").lower()

    print(f"Auth flow: {auth_flow}")
    print(f"Client ID: {client_id}")
    if (
        auth_flow == "client_credentials"
    ):  # print first two and last two of client secret
        print(
            f"Client secret: {os.environ['CLIENT_SECRET'][:2]}...{os.environ['CLIENT_SECRET'][-2:]}"
        )
    if auth_flow not in VALID_AUTH_FLOWS:
        raise ValueError(
            f"AUTH_FLOW must be one of {VALID_AUTH_FLOWS}, got '{auth_flow}'"
        )

    client = CogniteClient(
        ClientConfig(
            client_name=client_name,
            project=project,
            base_url=f"https://{cluster}.cognitedata.com",
            credentials=_get_credentials(cluster, tenant_id, client_id, auth_flow),
            api_subversion=api_subversion,
        )
    )

    token = client.iam.token.inspect()
    print(f"Connected as : {token.subject}")
    print(f"Project      : {project}")
    print(f"Auth flow    : {auth_flow}")

    return client
