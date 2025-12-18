from pathlib import Path
from gait.repo import GaitRepo


def test_repo_init_creates_layout(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    assert (tmp_path / ".gait").exists()
    assert (tmp_path / ".gait" / "objects").exists()
    assert (tmp_path / ".gait" / "refs" / "heads" / "main").exists()
    assert (tmp_path / ".gait" / "HEAD").exists()
