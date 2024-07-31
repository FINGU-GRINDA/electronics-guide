def lint():
    import subprocess

    subprocess.run("pyright ./app && ruff check . && black . --check", shell=True)


def lint_fix():
    import subprocess

    subprocess.run("pyright ./app && ruff . --fix && black .", shell=True)


def start():
    import subprocess

    subprocess.run(
        "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --loop asyncio",
        shell=True,
    )
