"""Utility functions for the Visual API."""

from pathlib import Path

from config import settings

# Network drive mappings for reading drawings
ENV_MOUNT_MAPPINGS = settings.NETWORK_MOUNT_MAPPINGS


def _parse_mappings(env_value: str) -> dict[str, str]:
    """
    Parse mappings like:
      //srvbhqpdm02/PDM_Vault_Bla=/mnt/srvbhqpdm02
    or multiple:
      //srvbhqpdm02/PDM_Vault_Bla=/mnt/srvbhqpdm02;//srvother/Share=Z:\
    Returns dict of normalized network-prefix -> local mount.
    """
    if not env_value:
        return {}
    out: dict[str, str] = {}

    for part in env_value.split(";"):
        part = part.strip()
        if not part:
            continue
        net, local = part.split("=", 1)
        # normalize network prefix for matching: use forward slashes, strip leading slashes, lowercase
        net_key = net.replace("\\", "/").lstrip("/").lower()
        out[net_key] = local

    return out


_NETWORK_MOUNT_MAPPINGS = _parse_mappings(ENV_MOUNT_MAPPINGS)


def map_network_to_local(orig_path: str) -> str:
    """
    Convert UNC path (any backslash/forward slash mix) to configured local mount.
    If no mapping matches, returns orig_path unchanged.
    """
    if not orig_path:
        return orig_path

    # preserve original-case normalized path for suffix extraction
    orig_norm = orig_path.replace("\\", "/").lstrip("/")
    norm = orig_norm.lower()

    # longest prefix first
    for net_prefix, local in sorted(
        _NETWORK_MOUNT_MAPPINGS.items(), key=lambda kv: -len(kv[0])
    ):
        if norm.startswith(net_prefix):
            # take suffix from orig_norm to preserve case
            suffix = orig_norm[len(net_prefix) :].lstrip("/")
            mapped = Path(local).joinpath(*([p for p in suffix.split("/") if p]))

            return str(mapped)

    return orig_path


def validate_mapped_path(mapped_path: str, allowed_mount: str | None = None) -> bool:
    """
    Ensure mapped_path is inside allowed_mount (if provided).
    If allowed_mount is None and there is exactly one mapping, use that mapping's local path.
    """
    try:
        mapped = Path(mapped_path).resolve()

        if allowed_mount is None:
            # if single mapping, use its value; otherwise require explicit allowed_mount
            if len(_NETWORK_MOUNT_MAPPINGS) == 1:
                allowed_mount = next(iter(_NETWORK_MOUNT_MAPPINGS.values()))
            else:
                return False

        allowed = Path(allowed_mount).resolve()

        return allowed == mapped or allowed in mapped.parents

    except Exception:
        return False
