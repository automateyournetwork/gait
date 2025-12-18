from pathlib import Path
from gait.repo import GaitRepo
from gait.schema import Turn


def test_merge_with_memory_unions_and_dedupes(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    # main: create + pin one turn
    _, c_main = repo.record_turn(Turn.v0("m1", "a1"))
    repo.pin_commit(c_main, note="main")

    main_mem_before = repo.read_memory_ref("main")
    main_items_before = repo.get_memory("main").items
    assert len(main_items_before) == 1

    # branch: create + pin another turn
    repo.create_branch("experiment")
    repo.checkout("experiment")
    _, c_exp = repo.record_turn(Turn.v0("e1", "b1"))
    repo.pin_commit(c_exp, note="exp")

    exp_items = repo.get_memory("experiment").items
    assert len(exp_items) == 2 or len(exp_items) == 1  # depending on inherit + pin behavior

    # merge into main with memory
    repo.checkout("main")
    merge_id = repo.merge("experiment", message="merge mem", with_memory=True)

    # main memory ref should change
    main_mem_after = repo.read_memory_ref("main")
    assert main_mem_after != main_mem_before

    # main memory should contain both turns (dedupe by turn_id)
    items = repo.get_memory("main").items
    turn_ids = [it.turn_id for it in items]
    assert len(set(turn_ids)) == len(turn_ids)
    assert len(items) >= 2  # union should bring at least one new pinned turn

    # merge commit meta should record memory merge details
    mc = repo.get_commit(merge_id)
    meta = mc.get("meta") or {}
    assert meta.get("memory_merged") is True
    assert meta.get("memory_target_before") == main_mem_before
    assert meta.get("memory_target_after") == main_mem_after
