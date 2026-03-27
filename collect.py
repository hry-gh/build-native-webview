#!/usr/bin/env python3

import argparse
import shutil
from pathlib import Path

CEF_PLATFORM_MAP = {
    "win-x64": "cef_windows_x86_64",
    "linux-x64": "cef_linux_x86_64",
    "osx-arm64": "cef_macos_aarch64",
    "osx-x64": "cef_macos_x86_64",
}

CEF_FILES_WINDOWS = [
    "libcef.dll", "chrome_elf.dll", "libEGL.dll", "libGLESv2.dll",
    "v8_context_snapshot.bin", "vk_swiftshader.dll", "vk_swiftshader_icd.json",
    "vulkan-1.dll", "icudtl.dat",
    "chrome_100_percent.pak", "chrome_200_percent.pak", "resources.pak",
]

CEF_FILES_LINUX = [
    "libcef.so", "libEGL.so", "libGLESv2.so",
    "libvk_swiftshader.so", "vk_swiftshader_icd.json",
    "v8_context_snapshot.bin", "icudtl.dat",
    "chrome_100_percent.pak", "chrome_200_percent.pak", "resources.pak",
]

MACOS_FLAT_LIBS = [
    "libEGL.dylib", "libGLESv2.dylib", "libvk_swiftshader.dylib", "vk_swiftshader_icd.json",
]


def find_cef_dir(release_dir: Path, cef_platform: str) -> Path | None:
    build_dir = release_dir / "build"
    if not build_dir.exists():
        return None
    for d in build_dir.iterdir():
        if d.name.startswith("cef-dll-sys-"):
            candidate = d / "out" / cef_platform
            if candidate.exists():
                return candidate
    return None


def main():
    parser = argparse.ArgumentParser(description="Collect native artifacts for a platform")
    parser.add_argument("--rid", required=True, choices=CEF_PLATFORM_MAP.keys())
    parser.add_argument("--triple", required=True)
    parser.add_argument("--webview-lib", required=True)
    parser.add_argument("--helper-bin", required=True)
    parser.add_argument("--target-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("artifact"))
    args = parser.parse_args()

    release_dir = args.target_dir / args.triple / "release"
    out = args.output / args.rid / "native"
    out.mkdir(parents=True, exist_ok=True)

    for name in [args.webview_lib, args.helper_bin]:
        src = release_dir / name
        if src.exists():
            shutil.copy2(src, out / name)
            print(f"Copied {name}")
        else:
            raise FileNotFoundError(f"{src} not found")

    cef_platform = CEF_PLATFORM_MAP[args.rid]
    cef_dir = find_cef_dir(release_dir, cef_platform)
    if cef_dir is None:
        raise RuntimeError(f"CEF directory not found for {args.rid}")

    print(f"CEF dir: {cef_dir}")

    if args.rid.startswith("osx"):
        fw_src = cef_dir / "Chromium Embedded Framework.framework"
        shutil.copytree(fw_src, out / "Chromium Embedded Framework.framework", symlinks=True)
        print("Copied framework bundle")

        for lib in MACOS_FLAT_LIBS:
            src = fw_src / "Libraries" / lib
            if src.exists():
                shutil.copy2(src, out / lib)
                print(f"Copied flat {lib}")

    elif args.rid.startswith("win"):
        for f in CEF_FILES_WINDOWS:
            src = cef_dir / f
            if src.exists():
                shutil.copy2(src, out / f)
        locales_src = cef_dir / "locales"
        if locales_src.exists():
            shutil.copytree(locales_src, out / "locales")
            print("Copied locales/")

    elif args.rid.startswith("linux"):
        for f in CEF_FILES_LINUX:
            src = cef_dir / f
            if src.exists():
                shutil.copy2(src, out / f)
        locales_src = cef_dir / "locales"
        if locales_src.exists():
            shutil.copytree(locales_src, out / "locales")
            print("Copied locales/")

    print(f"Done collecting {args.rid}")


if __name__ == "__main__":
    main()
