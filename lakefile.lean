import Lake
open Lake

package «so-hmns» where
  -- 전역 힙 메모리 및 연산 제약 영구 해제
  moreLeanArgs := #[
    "-DmaxHeartbeats=0",
    "-DmaxRecDepth=2000000"
  ]

@[default_target]
lean_lib SoHmns where
  -- [보완] 하위 Modules 폴더를 포함한 모든 고차 분할 가군 서브 디렉터리를 전역 빌드 타깃으로 강제 바인딩
  globs := #[.submodules `SoHmns]
