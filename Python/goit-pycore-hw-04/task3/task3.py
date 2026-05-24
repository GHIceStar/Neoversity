from pathlib import Path
import sys

from colorama import Fore, Style, init


init(autoreset=True)

DEBUG_DIRECTORY_PATH = Path(__file__).resolve().parent / "picture"


def print_directory_tree(path, prefix=""):
    items = sorted(
        path.iterdir(),
        key=lambda item: (not item.is_dir(), item.name.lower())
    )

    for index, item in enumerate(items):
        is_last = index == len(items) - 1
        connector = "┗ " if is_last else "┣ "
        next_prefix = prefix + "  " if is_last else prefix + "┃ "

        if item.is_dir():
            print(
                f"{prefix}{connector}"
                f"{Fore.BLUE}📂 {item.name}/{Style.RESET_ALL}"
            )
            print_directory_tree(item, next_prefix)
        else:
            print(
                f"{prefix}{connector}"
                f"{Fore.GREEN}📜 {item.name}{Style.RESET_ALL}"
            )


def validate_directory_path(path):
    if not path.exists():
        print(f"{Fore.RED}Error: Path does not exist.{Style.RESET_ALL}")
        return False

    if not path.is_dir():
        print(f"{Fore.RED}Error: Path is not a directory.{Style.RESET_ALL}")
        return False

    return True


def main():
    if len(sys.argv) == 2:
        directory_path = Path(sys.argv[1])
    else:
        directory_path = DEBUG_DIRECTORY_PATH
        print(
            f"{Fore.YELLOW}Debug mode: using default path: "
            f"{directory_path}{Style.RESET_ALL}"
        )

    if not validate_directory_path(directory_path):
        return

    print(f"{Fore.BLUE}📦 {directory_path.name}/{Style.RESET_ALL}")
    print_directory_tree(directory_path)


if __name__ == "__main__":
    main()