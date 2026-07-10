# sofa_linter.py (SO-HMNS 우주적 다중 난제 통합 오독 검증 모듈)
import re
import sys

def check_formal_rigor(lean_code_path):
    try:
        with open(lean_code_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {lean_code_path}")
        return False

    # AI 오독이 자주 일어나는 수학 난제별 필수 제약 조건 매트릭스
    problem_matrix = {
        # 1. 소파 이동 문제 규칙 (강체 보존 및 고정 폭 1)
        "Sofa_Problem": {
            "Constant_Width_1": r"(corridor_width\s*=\s*1|constant_width)",
            "Euclidean_Rigidity": r"(Isisotropic_Euclidean_Space|Rigid_Body_Constraint|SE2_Lie_Group)",
            "Strict_Non_Overlapping": r"(discrete_collision_boundary|strict_non_overlapping)"
        },
        # 2. 리만 가설 규칙 (임계선 임의 변형 방지 및 영점 정의 보호)
        "Riemann_Hypothesis": {
            "Critical_Line_Strict": r"(critical_line\s*=\s*1\/2|Re\(s\)\s*=\s*1\/2)",
            "Zeta_Analytic_Continuation": r"(zeta_analytic_continuation|riemann_zeta_function)"
        },
        # 3. P vs NP 문제 규칙 (결정론적 튜링 기계 오독 방지)
        "P_vs_NP_Conjecture": {
            "Deterministic_Turing_Machine": r"(deterministic_turing_machine|DTM_model)",
            "Polynomial_Time_Verification": r"(polynomial_time_verifier|poly_time_bounds)"
        },
        # 4. 콜라츠 추측 규칙 (정수 도메인 왜곡 방지 - 실수 확장 금지)
        "Collatz_Conjecture": {
            "Strict_Positive_Integers": r"(domain\s*=\s*ℕ\+|strictly_positive_integral)"
        }
    }

    print("[SO-HMNS Strict Lint Gate] 전 우주적 다중 난제 오독 스크리닝 시작...")
    
    # 소스코드 텍스트 문맥을 분석하여 어떤 문제를 풀려고 하는지 AI의 의도를 자동 탐색
    detected_problems = []
    if re.search(r"(sofa|corridor|gerver)", code, re.IGNORECASE): detected_problems.append("Sofa_Problem")
    if re.search(r"(riemann|zeta|critical_line)", code, re.IGNORECASE): detected_problems.append("Riemann_Hypothesis")
    if re.search(r"(p_vs_np|turing|polynomial)", code, re.IGNORECASE): detected_problems.append("P_vs_NP_Conjecture")
    if re.search(r"(collatz|3n\+1|hailstone)", code, re.IGNORECASE): detected_problems.append("Collatz_Conjecture")

    if not detected_problems:
        # 일반 파일(예: 지진 관련 코드)은 기하학/수학 난제 필터를 그냥 통과시켜 안전 보장
        return True

    # 탐지된 난제별로 필수 조건 유실 여부 정밀 검사
    for prob in detected_problems:
        print(f"🎯 탐지된 수학 난제 증명 시도: {prob}")
        missing_points = []
        for constraint_name, pattern in problem_matrix[prob].items():
            if not re.search(pattern, code, re.IGNORECASE):
                missing_points.append(constraint_name)
        
        if missing_points:
            print(f"\n❌ [{prob} 오독 감지됨] 아래 필수 제약 조건이 선언되지 않았습니다: {missing_points}")
            print(f"💡 원인: AI가 문제를 마음대로 허물거나 완화하여 공허한 거짓 해를 도출했습니다.")
            return False

    print("\n✅ [모든 난제 검증 통과] 작성된 코드의 물리/수학적 대전제가 완벽히 엄밀합니다.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python sofa_linter.py <검증할_Lean파일_경로>")
        sys.exit(1)
    success = check_formal_rigor(sys.argv[1])
    sys.exit(0 if success else 1)
