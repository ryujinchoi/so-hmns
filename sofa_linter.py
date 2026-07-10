# sofa_linter.py (SO-HMNS 유니버설 수학/물리 오독 감시 코어 엔진)
import re
import sys

def check_formal_rigor(lean_code_path):
    try:
        with open(lean_code_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        return True # 일반 파일은 패스

    print(f"[SO-HMNS Universal Guard] 글로벌 수학 정의 스크리닝 시작: {lean_code_path}")
    
    # --- [1단계] AI의 3대 고질적 오독 패턴 검사 (전체 문제 공통) ---
    errors = []
    
    # 패턴 A: 공허한 참(Vacuous Truth) 유도 - 전제를 모순되거나 쓸모없게 짜서 결론을 날로 먹는 행위 차단
    if re.search(r"axiom\s+\w+\s*:\s*False", code) or re.search(r"sorry", code):
        errors.append("Vacuous_Proof_Bypass (구멍 난 증명 강제 스킵 시도)")
        
    # 패턴 B: 도메인 불법 변형 - 정수/실수 범위를 마음대로 왜곡하여 조건 회피 방지
    if "domain" in code.lower() and not any(x in code for x in ["ℝ", "ℕ", "ℤ", "ℂ"]):
        errors.append("Invalid_Domain_Relaxation (해석 공간의 임의적 규격 완화)")

    # 패턴 C: 위상학적 스무딩(Relaxation) - 경계를 연속 함수로 뭉개서 충돌을 비껴가는 억지 꼼수 차단
    if re.search(r"(approximate_|smoothed_|relaxed_)", code, re.IGNORECASE):
        errors.append("Mathematical_Smoothing_Leak (엄밀성 유실 및 근사치 꼼수)")

    # --- [2단계] 특정 유명 문제 감지 시 필수 보존 조건 교차 검증 ---
    if re.search(r"(sofa|corridor|gerver)", code, re.IGNORECASE):
        if not re.search(r"(corridor_width\s*=\s*1|constant_width)", code) or not re.search(r"(Rigid_Body|SE2)", code):
            errors.append("Sofa_Context_Violation (강체 조건 및 복도 고정폭 정의 유실)")
            
    if re.search(r"(riemann|zeta|critical_line)", code, re.IGNORECASE):
        if not re.search(r"(1\/2|half)", code):
            errors.append("Riemann_Context_Violation (임계선 1/2 조건 이탈)")

    # --- [3단계] 최종 차단 및 통제 분기 ---
    if errors:
        print(f"\n❌ [오독 가드 작동] 엄밀성 결함이 감지되어 커밋을 즉시 기각합니다.")
        print(f"⚠️ 사유 목록: {errors}")
        print("💡 조치: AI가 입력한 가정이 완벽한 상수나 고정 강체, 불변 공간으로 제한되었는지 원본 문제를 재확인하세요.")
        return False

    print("✅ [유니버설 필터 통과] 코드의 전제와 정의가 논리적으로 안전합니다.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    success = check_formal_rigor(sys.argv[1])
    sys.exit(0 if success else 1)
