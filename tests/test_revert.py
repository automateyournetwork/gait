from pathlib import Path
from gait.repo import GaitRepo
from gait.schema import Turn


def test_revert_moves_head_back_one_commit(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    _, c1 = repo.record_turn(Turn.v0("Q1", "A1"))
    _, c2 = repo.record_turn(Turn.v0("Q2", "A2"))

    assert repo.head_commit_id() == c2

    # revert to parent of HEAD (should be c1)
    c2_obj = repo.get_commit(c2)
    parent = (c2_obj.get("parents") or [None])[0]
    assert parent == c1

    repo.reset_branch(c1)
    assert repo.head_commit_id() == c1
