import asyncio
import ctypes
import subprocess
from sys import argv, exit

from hyper_switcher.consts import ARGS_ERROR_MSG, HELP_MSG, NEED_RESTART_CODE, VMP, WSL
from termcolor import colored


def make_commands(switcher: str):
    return [
        (
            f"dism.exe /online /{switcher}-feature /featurename:{WSL} {'/all' if switcher == 'enabled' else ''} /norestart /english",
            WSL,
        ),
        (
            f"dism.exe /online /{switcher}-feature /featurename:{VMP} {'/all' if switcher == 'enabled' else ''} /norestart /english",
            VMP,
        ),
    ]


async def animate_progress_msg():
    try:
        while True:
            for i in range(4):
                print(f"\rExecuting{'.' * i}{' ' * (3 - i)}", end="")
                await asyncio.sleep(0.2)
    except asyncio.CancelledError:
        pass


def is_feature_enabled(feature_name: str) -> bool:
    result = subprocess.run(
        [
            "dism.exe",
            "/online",
            "/Get-FeatureInfo",
            "/english",
            f"/featurename:{feature_name}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return "Enabled" in result.stdout


async def run_command(commands: list, expected_value: bool):
    reboot_flag = False
    for command in commands:
        if expected_value == is_feature_enabled(command[1]):
            task = asyncio.create_task(animate_progress_msg())
            process = await asyncio.create_subprocess_shell(
                command[0],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            task.cancel()

            if process.returncode == NEED_RESTART_CODE:  # 3010
                print(colored(f"\tExecuting for {command[1]} success", "cyan"))
                reboot_flag = True
            elif process.returncode != 0:
                print(
                    f"\n{colored('Error:', 'red')} command {command[0]} return {stderr.decode()}"
                )
        else:
            print(
                colored(
                    f"\nCommand skipped. {command[1]} already {'deactivated' if expected_value else 'activated'}. Try reboot your PC",
                    "yellow",
                )
            )

    if reboot_flag:
        reboot()


def reboot():
    user_input = input(colored("You need to reboot PC? (Y/N): ", "yellow"))

    match user_input:
        case "Y" | "y":
            print(colored("Rebooting...", "red", attrs=["bold"]))
            subprocess.run("shutdown /r /t 0", shell=True)
        case _:
            print(colored("You should reboot it later.", "yellow"))


def check_permissions():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print(colored("You must run as administrator", "red", attrs=["bold"]))
        exit(0)


def main():
    args = argv

    match args:
        case [_, "-h"]:
            print(HELP_MSG)
        case [_, "-s"]:
            check_permissions()
            print(
                f"Status:\n"
                f"  {WSL}: {colored(is_feature_enabled(WSL), 'cyan')}\n"
                f"  {VMP}: {colored(is_feature_enabled(VMP), 'cyan')}"
            )
        case [_, "-e"]:
            check_permissions()
            asyncio.run(run_command(make_commands("enable"), expected_value=False))
        case [_, "-d"]:
            check_permissions()
            asyncio.run(run_command(make_commands("disable"), expected_value=True))
        case [_, "-eW"]:
            check_permissions()
            asyncio.run(run_command([make_commands("enable")[0]], expected_value=False))
        case [_, "-eV"]:
            check_permissions()
            asyncio.run(run_command([make_commands("enable")[1]], expected_value=False))
        case [_, "-dW"]:
            check_permissions()
            asyncio.run(run_command([make_commands("disable")[0]], expected_value=True))
        case [_, "-dV"]:
            check_permissions()
            asyncio.run(run_command([make_commands("disable")[1]], expected_value=True))
        case _:
            print(f"\n{ARGS_ERROR_MSG}\n{HELP_MSG}")


if __name__ == "__main__":
    main()
