import importlib
from pathlib import Path



def reload_util_with_env(monkeypatch, env_value: str):
    monkeypatch.setenv("PDM_MOUNT_MAPPINGS", env_value)
    import visualapi.util as util  # import after conftest has added src
    importlib.reload(util)
    return util


def test_parse_mappings_single(monkeypatch):
    util = reload_util_with_env(monkeypatch, "//srvbhqpdm02/PDM_Vault_Bla=/mnt/srvbhqpdm02")
    parsed = util._parse_mappings("//srvbhqpdm02/PDM_Vault_Bla=/mnt/srvbhqpdm02")
    assert parsed == {"srvbhqpdm02/pdm_vault_bla": "/mnt/srvbhqpdm02"}


def test_map_network_to_local_basic(monkeypatch):
    util = reload_util_with_env(monkeypatch, "//srvbhqpdm02/PDM_Vault_Bla=/mnt/srvbhqpdm02")
    unc = r"\\srvbhqpdm02\PDM_Vault_Bla\dir\file.PDF"
    mapped = util.map_network_to_local(unc)
    expected = str(Path("/mnt/srvbhqpdm02").joinpath("dir", "file.PDF"))
    assert mapped == expected


def test_validate_mapped_path_allowed_and_disallowed(monkeypatch, tmp_path):
    allowed = tmp_path / "mount"
    (allowed / "sub").mkdir(parents=True)
    f = allowed / "sub" / "file.PDF"
    f.write_text("ok")

    util = reload_util_with_env(monkeypatch, f"//srvbhqpdm02/PDM_Vault_Bla={allowed}")
    mapped = util.map_network_to_local(r"\\srvbhqpdm02\PDM_Vault_Bla\sub\file.PDF")
    assert util.validate_mapped_path(mapped, allowed_mount=str(allowed)) is True

    # when there are multiple mappings and allowed_mount omitted, validation should fail
    util_multi = reload_util_with_env(monkeypatch, "//a/one=/tmp/a;//b/two=/tmp/b")
    assert util_multi.validate_mapped_path(str(allowed)) is False