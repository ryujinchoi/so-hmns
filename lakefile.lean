import Lake
open Lake

package «so-hmns» where
  moreLeanArgs := #[
    "-DmaxHeartbeats=0",
    "-DmaxRecDepth=2000000"
  ]

@[default_target]
lean_lib SoHmns where
  -- 폴더 루트에 위치한 파일과 하위 서브디렉토리 모듈 전체를 빌드 타깃으로 연립 바인딩
  globs := #[.andSubmodules `SoHmns]
