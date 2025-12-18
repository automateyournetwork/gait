from pathlib import Path

from gait.repo import GaitRepo
from gait.schema import Turn


def test_revert_also_memory_rewinds_pins(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    # baseline commit + pin
    _, c1 = repo.record_turn(Turn.v0("Q1", "A1"), message="baseline")
    mem1 = repo.pin_commit(c1, note="baseline")

    assert repo.read_ref("main") == c1
    assert repo.read_memory_ref("main") == mem1
    assert len(repo.get_memory("main").items) == 1

    # bad commit + pin
    _, c2 = repo.record_turn(Turn.v0("Q2", "A2 (bad)"), message="bad")
    mem2 = repo.pin_commit(c2, note="oops pinned bad")

    assert repo.read_ref("main") == c2
    assert repo.read_memory_ref("main") == mem2
    assert len(repo.get_memory("main").items) == 2

    # revert HEAD back to baseline commit
    repo.reset_branch(c1)
    assert repo.read_ref("main") == c1

    # now rewind memory to match HEAD
    old_mem, new_mem = repo.rewind_memory_to_head(branch="main", head_commit=repo.read_ref("main"))

    assert old_mem == mem2
    assert new_mem == mem1
    assert repo.read_memory_ref("main") == mem1

    manifest = repo.get_memory("main")
    assert len(manifest.items) == 1
    assert manifest.items[0].note == "baseline"
