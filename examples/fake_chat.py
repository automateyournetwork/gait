from gait.repo import GaitRepo
from gait.schema import Turn

def main():
    repo = GaitRepo.discover()
    print(f"GAIT repo found at: {repo.root}")

    while True:
        user = input("\nYou> ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        # fake "model"
        assistant = f"(fake) You said: {user}"

        turn = Turn.v0(
            user_text=user,
            assistant_text=assistant,
            model={"provider": "fake", "model": "echo-v0"},
        )
        turn_id, commit_id = repo.record_turn(turn, message="fake_chat")
        print(f"AI> {assistant}")
        print(f"[gait] turn={turn_id[:8]} commit={commit_id[:8]} branch={repo.current_branch()}")

if __name__ == "__main__":
    main()
