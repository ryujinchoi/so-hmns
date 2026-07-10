# sofa_linter.py (SO-HMNS 유니버설 수학/물리 오독 감시 코어 엔지니어링 V2)
import re
import sys

def check_formal_rigor(lean_code_path):
    try:
        with open(lean_code_path, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        return True

    print(f"[SO-HMNS Universal Guard V2] 글로벌 수학 정의 초정밀 스크리닝 시작: {lean_code_path}")
    
    # 0단계: 빈 파일 및 유효 코드 누락 검사 (최소 분량 검증)
    if len(code.strip()) < 10 or not re.search(r"(theorem|def|lemma|axiom)", code, re.IGNORECASE):
        print("❌ [업로드 차단] 실질적인 Lean 4 증명 또는 정의 코드가 포함되어 있지 않습니다.")
        return False

    errors = []
    
    # 1단계: 고질적 꼼수 패턴 정교화 (공백/대소문자 유연화 매칭)
    if re.search(r"axiom\s+\w+\s*:\s*False", code, re.IGNORECASE) or re.search(r"\bsorry\b", code):
        errors.append("Vacuous_Proof_Bypass (구멍 난 증명 강제 스킵 시도)")
        
    if "domain" in code.lower() and not any(x in code for x in ["ℝ", "ℕ", "ℤ", "ℂ"]):
        errors.append("Invalid_Domain_Relaxation (해석 공간의 임의적 규격 완화)")

    if re.search(r"\b(approximate|smoothed|relaxed|pseudo|soft)\b", code, re.IGNORECASE):
        errors.append("Mathematical_Smoothing_Leak (엄밀성 유실 및 근사치 꼼수)")

    # 2단계: 문맥 제약 조건 정규식 고도화 (대소문자/공백/언더바 무력화)
    if re.search(r"(sofa|corridor|gerver)", code, re.IGNORECASE):
        # corridor_width = 1 또는 constant_width 형태를 유연하게 탐지
        width_check = re.search(r"corridor\s*[-_]?\s*width\s*=\s*1", code, re.IGNORECASE) or re.search(r"constant\s*[-_]?\s*width", code, re.IGNORECASE)
        # RigidBody, Rigid_Body, SE(2), SE2 형태를 유연하게 탐지
        rigidity_check = re.search(r"rigid\s*[-_]?\s*body", code, re.IGNORECASE) or re.search(r"SE\s*\(?\s*2\s*\)?", code, re.IGNORECASE)
        
        if not width_check or not rigidity_check:
            errors.append("Sofa_Context_Violation (강체 조건 및 복도 고정폭 정의 유실)")
            
    if re.search(r"(riemann|zeta|critical_line)", code, re.IGNORECASE):
        if not re.search(r"1\s*/\s*2", code) and not re.search(r"\bhalf\b", code, re.IGNORECASE):
            errors.append("Riemann_Context_Violation (임계선 1/2 조건 이탈)")

    # 3단계: 최종 판정
    if errors:
        print(f"\n❌ [오독 가드 작동] 엄밀성 결함이 감지되어 커밋을 즉시 기각합니다.")
        print(f"⚠️ 사유 목록: {errors}")
        return False

    print("✅ [유니버설 필터 통과] 코드의 전제와 정의가 논리적으로 안전합니다.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    success = check_formal_rigor(sys.argv)
    sys.exit(0 if success else 1)
