from pathlib import Path
from gait.repo import GaitRepo
from gait.schema import Turn


def test_memory_created_on_init(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()
    # should exist and point to an object
    mem_ref = tmp_path / ".gait" / "refs" / "memory" / "main"
    assert mem_ref.exists()
    assert mem_ref.read_text().strip()


def test_pin_and_unpin(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    t = Turn.v0("u", "a")
    _, c = repo.record_turn(t)

    mem_id = repo.pin_commit(c, note="keep this")
    m = repo.get_memory()
    assert len(m.items) == 1
    assert m.items[0].note == "keep this"

    repo.unpin_index(1)
    m2 = repo.get_memory()
    assert len(m2.items) == 0


def test_branch_inherits_memory(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    # add a commit and pin it on main
    t = Turn.v0("u", "a")
    _, c = repo.record_turn(t)
    repo.pin_commit(c, note="pinned on main")

    # create branch and verify memory ref matches
    repo.create_branch("feat")
    main_mem = repo.read_memory_ref("main")
    feat_mem = repo.read_memory_ref("feat")
    assert main_mem == feat_mem
