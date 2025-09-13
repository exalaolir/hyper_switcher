from termcolor import colored

HELP_MSG = f"""
{colored("Use to enable or disable WSL or VirtualMachinePlatform. Always run as administrator.", "yellow")}

{colored("Commands:", "cyan")}
  {colored("-h", "green")}      -- Help.
  {colored("-e", "green")}      -- Enable all
  {colored("-d", "green")}      -- Disable all.
  {colored("-eW", "green")}     -- Enable WSL.
  {colored("-dW", "green")}     -- Disable WSL.
  {colored("-eV", "green")}     -- Enable VirtualMachinePlatform.
  {colored("-dV", "green")}     -- Disable VirtualMachinePlatform.
  {colored("-s", "green")}      -- Status
"""

ARGS_ERROR_MSG = colored(
    "Invalid args. You can use only one arg from command list.", "red", attrs=["bold"]
)

WSL = "Microsoft-Windows-Subsystem-Linux"

VMP = "VirtualMachinePlatform"

NEED_RESTART_CODE = 3010
