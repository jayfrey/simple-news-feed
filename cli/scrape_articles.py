import argparse
import os
import time
import textwrap

import utils.docker_compose_commands as dcm


def run_crawler(source):
    command = [
        "run",
        "crawler",
        "scrapy",
        "crawl",
        source,
    ]

    command_string = " ".join(command)
    print(command_string)

    execute_command = f"{dcm.get_docker_compose_command(args)} {command_string}"
    print(execute_command)
    return os.system(execute_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--docker-compose-command",
        default="docker-compose",
        help=textwrap.dedent(
            """\
                Specify docker-compose command. 
                Default: docker-compose
            """,
        ),
    )
    parser.add_argument(
        "--docker-compose-file",
        default="docker-compose.yml",
        help=textwrap.dedent(
            """\
                Specify docker-compose file. 
                Default: docker-compose.yml
            """,
        ),
    )
    parser.add_argument(
        "-s",
        "--sources",
        nargs="+",
        type=str,
        default=["says", "free_malaysia_today", "berita_harian"],
        help=textwrap.dedent(
            """\
                Specify one or more sources to run crawler to scrape articles. 
                By default, it will scrape all of the sources.
                Supported sources: says, free_malaysia_today or berita_harian
            """,
        ),
    )

    args = parser.parse_args()
    os.chdir(os.path.dirname(os.path.dirname(__file__)))

    dcm.start_docker_compose(args, ["up", "-d", "postgres"])
    print(args)

    print("Sleep for 10s to make sure it is started porperly")
    time.sleep(10)

    for source in args.sources:
        run_crawler(source)
