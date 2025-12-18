from pathlib import Path
from gait.repo import GaitRepo
from gait.schema import Turn


def test_context_bundle_contains_pinned_turns(tmp_path: Path):
    repo = GaitRepo(root=tmp_path)
    repo.init()

    t = Turn.v0("hello", "hi")
    _, c = repo.record_turn(t, message="m1")

    repo.pin_commit(c, note="keeper")

    bundle = repo.build_context_bundle(full=False)
    assert bundle["schema"] == "gait.context.v0"
    assert bundle["pinned_items"] == 1
    assert bundle["items"][0]["note"] == "keeper"
    assert bundle["items"][0]["user_text"] == "hello"
    assert bundle["items"][0]["assistant_text"] == "hi"
