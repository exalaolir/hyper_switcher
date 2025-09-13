<h1 align="center">Hyperswitcher</h1>

### Description

This utility is used to toggle VirtualMachinePlatform and WSL. I created it because I frequently need to switch between Docker (which requires these features) and VirtualBox (which runs slower when VirtualMachinePlatform is enabled).

### Commands

- -h      -- Help(you can use this without admin permissions).
- -e      -- Enable all
- -d      -- Disable all.
- -eW     -- Enable WSL.
- -dW     -- Disable WSL.
- -eV     -- Enable VirtualMachinePlatform.
- -dV     -- Disable VirtualMachinePlatform.
- -s      -- Status

> [!IMPORTANT]
> **You must run this script as administrator**

### Installation

> [!IMPORTANT]
> **You must have python>=3.13**

1. Download **hyperswitcher.whl** from the Releases section.
2. Open the terminal in the folder where you downloaded the **hyperswitcher.whl** file.
3. Run ```pip inslall hyperswitcher.whl```
