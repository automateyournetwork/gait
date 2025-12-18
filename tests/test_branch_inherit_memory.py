from pathlib import Path
from gait.repo import GaitRepo
from gait.schema import Turn


def test_branch_inherits_memory_by_default(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    _, c = repo.record_turn(Turn.v0("hello", "hi"))
    repo.pin_commit(c, note="baseline")

    main_mem = repo.read_memory_ref("main")
    assert main_mem  # should exist

    repo.create_branch("experiment")  # default: inherit memory
    exp_mem = repo.read_memory_ref("experiment")
    assert exp_mem == main_mem


def test_branch_can_disable_memory_inheritance(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    _, c = repo.record_turn(Turn.v0("hello", "hi"))
    repo.pin_commit(c, note="baseline")

    main_mem = repo.read_memory_ref("main")
    assert main_mem

    repo.create_branch("no_mem", inherit_memory=False)
    no_mem = repo.read_memory_ref("no_mem")

    # In this design, even "empty memory" is represented by a canonical manifest hash.
    assert no_mem
    assert no_mem != main_mem

    manifest = repo.get_memory("no_mem")
    assert len(manifest.items) == 0
