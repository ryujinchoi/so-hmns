import Lake
open Lake Lean

package «so-hmns» {
  -- Add package configuration options here
}

lean_lib «SoHmnsInvariants» {
  -- Add library configuration options here
}

@[default_target]
lean_exe «so-hmns» {
  root := `Main
}

require mathlib from git
  "https://github.com"
