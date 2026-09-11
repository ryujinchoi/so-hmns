import Lake
open Lake Pure

package «so-hmns» where
  version := "1.0.0"

require mathlib from git
  "https://github.com" @ "v4.11.0"

@[default_target]
lean_lib «SoHmns» where
  srcDir := "."
  roots := #[`SoHmns.Basic]
