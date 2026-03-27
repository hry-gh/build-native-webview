# build-native-webview

CI pipeline to build the `Robust.Natives.Cef` NuGet package for [RobustToolbox](https://github.com/space-wizards/RobustToolbox).

This package contains pre-built native binaries for the Rust-based CEF (Chromium Embedded Framework) webview integration:

- `robust-native-webview` — Rust cdylib exposing a C FFI for .NET P/Invoke
- `cef-helper` — CEF subprocess helper binary
- CEF runtime files (framework, locales, ANGLE libraries, etc.)

## Platforms

| RID | Runner | Rust Target |
|-----|--------|-------------|
| `win-x64` | `windows-latest` | `x86_64-pc-windows-msvc` |
| `linux-x64` | `ubuntu-latest` | `x86_64-unknown-linux-gnu` |
| `osx-arm64` | `macos-14` | `aarch64-apple-darwin` |
| `osx-x64` | `macos-13` | `x86_64-apple-darwin` |

## Usage

Use the "Run workflow" button on the Actions tab to trigger a build. The resulting `.nupkg` is uploaded as an artifact.
