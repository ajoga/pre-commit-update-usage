# pre-commit-update-usage

[Pre-commit hooks](https://pre-commit.com) are tests that run each time you attempt to commit. If the tests pass, the commit will be made, otherwise not.

## Goal of this hook

Keep the "usage" section of your README up-to-date without thinking about it ever again.

## How to use

1. Get started with [pre-commit](https://pre-commit.com) by following their documentation.

2. Update your local `.pre-commit-config.yaml` with:

    ```yaml
    repos:
      - repo: /home/ssm-user/pre-commit-update-hook
        rev: main
        hooks:
          - id: update-usage
            args:
              [
                --usage-command=uptime,
              ]
    ```

3. Replace the placeholder `uptime` mention by the necessary command to get the usage of your program. This command will be passed to your shell for resolution. You don't need to escape spaces.

## Poetry usage

If you run your git command within shell spun up with `poetry shell`, then when `pre-commit` will execute this hook, the current virtual environment will be overriden by `pre-commit`'s. Setting `--usage-command poetry run yourcommand` **will not** set the current virtual environment to the one you expect because poetry will not replace a virtual environment by its own (see [this issue](https://github.com/python-poetry/poetry/issues/5323)).

The best thing I found working so far is this:

1. Create a `poetry.toml` with:

    ```toml
    [virtualenvs]
    in-project = true
    ```

2. Exit your poetry shell
3. Find your current poetry installation with `poetry env info --path`
4. Delete it fully with `rm -fr`
5. Create the local `.venv` folder
6. Run `poetry install` and make sure it installs in the local .venv folder
7. Observe the above arguments in `.pre-commit-config.yaml`:

    ```yaml
      - repo: /home/ssm-user/pre-commit-update-hook
        rev: main
        hooks:
          - id: update-usage
            args:
              [
                --usage-command=source .venv/bin/activate && poetry run python src/main.py --help,
              ]
    ```

## Usage and demo

The usage of the pre-commit hook above is generated by using itself :) :

<!-- usage snippet start -->
```shell
usage: main.py [-h] --usage-command USAGE_COMMAND [--readme-path README_PATH]

options:
  -h, --help            show this help message and exit
  --usage-command USAGE_COMMAND
                        Command to run to get the usage to put in the README
  --readme-path README_PATH
                        Path to the README file. Defaults to ./README.md

```
<!-- usage snippet end -->