from pathlib import Path
from gait.repo import GaitRepo
from gait.schema import Turn

def test_merge_creates_two_parent_commit(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    # main commit
    t1 = Turn.v0("hi", "hello")
    _, c1 = repo.record_turn(t1)

    # branch off
    repo.create_branch("experiment")
    repo.checkout("experiment")
    t2 = Turn.v0("branch", "work")
    _, c2 = repo.record_turn(t2)

    # merge into main
    repo.checkout("main")
    merge_id = repo.merge("experiment")

    c = repo.get_commit(merge_id)
    assert c["kind"] == "merge"
    assert c["parents"] == [c1, c2]
