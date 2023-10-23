import subprocess
import argparse

OPEN_TAG = "<!-- usage snippet start -->"
CLOSE_TAG = "<!-- usage snippet end -->"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--usage-command", help="Command to run to get the usage to put in the README", required=True)
    parser.add_argument("--readme-path", help="Path to the README file. Defaults to ./README.md", default="./README.md")
    args = parser.parse_args()

    usage = subprocess.run(
        args.usage_command,
        check=True,
        stdout=subprocess.PIPE,
        shell=True,
    )

    try:
        with open(args.readme_path, "r", encoding="utf-8") as readme:
            file_content = readme.read()
    except FileNotFoundError as error:
        print(error.strerror)
        exit(code=1)

    # ensure we have one of each opening / closing tag and no more
    if OPEN_TAG not in file_content:
        print(f"Could not find the opening tag: {OPEN_TAG}")
        exit(code=1)
    if CLOSE_TAG not in file_content:
        print(f"Could not find the closing tag: {CLOSE_TAG}")
        exit(code=1)

    if file_content.count(OPEN_TAG) > 1 or file_content.count(CLOSE_TAG) > 1:
        print("Found more than one opening or closing tag, please ensure there is exactly one of each.")
        exit(code=1)

    header, _, footer = file_content.partition(OPEN_TAG)
    _, _, footer = footer.partition(CLOSE_TAG)

    out = (
            header +
            OPEN_TAG +
            '\n'+ 
            '```shell' + 
            '\n'+ 
            usage.stdout.decode() +
            '\n' +
            '```' +
            '\n' +
            CLOSE_TAG +
            footer
          )

    if out != file_content:
        print("The usage of the README has changed, updating")
        with open(args.readme_path, "w", encoding="utf-8") as readme:
            readme.write(out)
        exit(code=1)

if __name__ == "__main__":
    main()