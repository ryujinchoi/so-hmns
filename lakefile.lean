import Lake
open Lake

package soHmns where
  moreLeanArgs := #[
    "-DmaxHeartbeats=0",
    "-DmaxRecDepth=1000000"
  ]

@[default_target]
lean_lib SoHmns where
  srcDir := "."
