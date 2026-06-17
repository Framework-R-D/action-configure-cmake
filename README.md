# `action-configure-cmake`

> Configures CMake with preset detection and customizable options. **Requires the `phlex-ci` container** (sources `/entrypoint.sh` to activate the Spack environment).

## Usage

```yaml
- uses: Framework-R-D/action-configure-cmake@e9abed19c06a2eedfed90c1f39f3a875cf206ec3 # v1
  with:
    input-name: value
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `preset` | CMake preset to use (e.g., coverage, default) | false | `default` |
| `source-path` | Path where source code is checked out | false | `phlex-src` |
| `build-path` | Path for build directory | false | `phlex-build` |
| `build-type` | CMake build type (Release, Debug, etc.) [do not use with coverage presets] | false | `` |
| `extra-options` | Additional CMake configuration options | false | `` |
| `enable-form` | Enable FORM support | false | `ON` |
| `form-root-storage` | Enable FORM root storage | false | `ON` |
| `form-rntuple-storage` | Enable FORM RNTuple storage | false | `ON` |
| `generator` | Specify CMake generator | false | `Ninja` |
| `cpp-compiler` | The C++ compiler to use | false | `g++` |

## Outputs

| Name | Description |
|------|-------------|
(none)

## License

[Apache 2.0](LICENSE)

## Notes

> [!NOTE]
> This action requires the `ghcr.io/framework-r-d/phlex-ci` container image
> (sources `/entrypoint.sh` to activate the Spack environment).
> It is not a general-purpose action.
