from pathlib import Path
from gait.repo import GaitRepo
from gait.schema import Turn


def test_record_turn_auto_commit(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    turn = Turn.v0("hi", "hello")
    turn_id, commit_id = repo.record_turn(turn)

    assert turn_id
    assert commit_id
    assert repo.head_commit_id().strip() == commit_id

    c = repo.get_commit(commit_id)
    assert c["schema"] == "gait.commit.v0"
    assert c["turn_ids"] == [turn_id]
    assert c["parents"] == []  # first commit on empty main
