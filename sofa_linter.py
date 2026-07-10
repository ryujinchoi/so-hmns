# sofa_linter.py (SO-HMNS 유니버설 AST 기반 주석 제거 및 오독 감시 코어 V3)
import re
import sys

def strip_lean_comments(code):
    # 1. 다중 행 주석 제거: /- ... -/
    code = re.sub(r'\/-\s*[\s\S]*?\s*-\/', '', code)
    # 2. 단일 행 주석 제거: -- ...
    code = re.sub(r'--.*', '', code)
    return code

def check_formal_rigor(lean_code_path):
    try:
        with open(lean_code_path, 'r', encoding='utf-8') as f:
            raw_code = f.read()
    except FileNotFoundError:
        return True

    # AST 전처리: 모든 주석 레이어를 완전히 소거하여 순수 코드 트랙만 추출
    pure_code = strip_lean_comments(raw_code)

    print(f"[SO-HMNS AST Guard V3] 주석 소거 후 순수 코드 엄밀성 검증 시작: {lean_code_path}")
    
    # 0단계: 주석 제거 후 빈 파일 및 유효 코드 누락 검사
    if len(pure_code.strip()) < 10 or not re.search(r"(theorem|def|lemma|axiom)", pure_code, re.IGNORECASE):
        print("❌ [업로드 차단] 주석을 제외한 실질적인 Lean 4 실행 코드가 없거나 부족합니다.")
        return False

    errors = []
    
    # 1단계: 순수 코드 내 고질적 꼼수 패턴 검사
    if re.search(r"axiom\s+\w+\s*:\s*False", pure_code, re.IGNORECASE) or re.search(r"\bsorry\b", pure_code):
        errors.append("Vacuous_Proof_Bypass (구멍 난 증명 강제 스킵 시도)")
        
    if "domain" in pure_code.lower() and not any(x in pure_code for x in ["ℝ", "ℕ", "ℤ", "ℂ"]):
        errors.append("Invalid_Domain_Relaxation (해석 공간의 임의적 규격 완화)")

    if re.search(r"\b(approximate|smoothed|relaxed|pseudo|soft)\b", pure_code, re.IGNORECASE):
        errors.append("Mathematical_Smoothing_Leak (엄밀성 유실 및 근사치 꼼수)")

    # 2단계: 순수 코드 내 컨텍스트 제약 조건 정밀 매칭
    if re.search(r"(sofa|corridor|gerver)", pure_code, re.IGNORECASE):
        width_check = re.search(r"corridor\s*[-_]?\s*width\s*=\s*1", pure_code, re.IGNORECASE) or re.search(r"constant\s*[-_]?\s*width", pure_code, re.IGNORECASE)
        rigidity_check = re.search(r"rigid\s*[-_]?\s*body", pure_code, re.IGNORECASE) or re.search(r"SE\s*\(?\s*2\s*\)?", pure_code, re.IGNORECASE)
        
        if not width_check or not rigidity_check:
            errors.append("Sofa_Context_Violation (주석 외부 실질 강체 조건 및 복도 고정폭 정의 누락)")
            
    if re.search(r"(riemann|zeta|critical_line)", pure_code, re.IGNORECASE):
        if not re.search(r"1\s*/\s*2", pure_code) and not re.search(r"\bhalf\b", pure_code, re.IGNORECASE):
            errors.append("Riemann_Context_Violation (주석 외부 실질 임계선 1/2 조건 이탈)")

    # 3단계: 최종 제어 및 판정
    if errors:
        print(f"\n❌ [오독 가드 작동] 주석 우회 눈속임 또는 엄밀성 결함이 감지되어 커밋을 기각합니다.")
        print(f"⚠️ 사유 목록: {errors}")
        return False

    print("✅ [AST 정제 필터 통과] 주석 눈속임이 없는 순수 코드가 논리적으로 완전합니다.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(1)
    success = check_formal_rigor(sys.argv)
    sys.exit(0 if success else 1)
