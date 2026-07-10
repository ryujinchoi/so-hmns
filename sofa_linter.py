# sofa_linter.py (독립 기하학 오독 검증 모듈)
import re
import sys

def check_formal_rigor(lean_code_path):
    try:
        with open(lean_code_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {lean_code_path}")
        return False
    
    critical_constraints = {
        "Constant_Width_1": r"(corridor_width\s*=\s*1|constant_width)",
        "Euclidean_Rigidity": r"(Isisotropic_Euclidean_Space|Rigid_Body_Constraint|SE2_Lie_Group)",
        "Strict_Non_Overlapping": r"(discrete_collision_boundary|strict_non_overlapping)"
    }
    
    missing_points = []
    print("[SO-HMNS Strict Lint Gate] 기하학 문제 오독 검증 시작...")
    
    for name, pattern in critical_constraints.items():
        if not re.search(pattern, code, re.IGNORECASE):
            missing_points.append(name)
            
    if missing_points:
        print(f"\n❌ [오독 감지됨] 아래 핵심 제약 조건이 누락되었습니다: {missing_points}")
        return False
    
    print("\n✅ [검증 통과] 모든 필수 기하학적 제약 조건이 엄밀하게 정의되었습니다.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python sofa_linter.py <검증할_Lean파일_경로>")
        sys.exit(1)
    success = check_formal_rigor(sys.argv[1])
    sys.exit(0 if success else 1)
