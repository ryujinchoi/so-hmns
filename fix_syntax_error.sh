#!/bin/bash
echo "[+] 파이썬 클래스 이름 공백 문법 오류 수정을 시작합니다..."

# 1. 원본 파일에서 공백이 포함된 클래스명을 올바른 파이썬 식별자(Academic_Integrity_Infrastructure)로 강제 치환
if [ -f "so_hmns_universal.py" ]; then
    sed -i 's/class Academic 무결성인프라:/class Academic_Integrity_Infrastructure:/g' so_hmns_universal.py
    echo "[*] so_hmns_universal.py 클래스 식별자 수정 완료."
fi

# 2. 커널 엔진(sohmnscore.py)에서 호출하던 부분도 공백이 없는 이름으로 동시 수정
if [ -f "sohmnscore.py" ]; then
    sed -i 's/aca_guard = Academic무결성인프라(/aca_guard = Academic_Integrity_Infrastructure(/g' sohmnscore.py
    echo "[*] sohmnscore.py 커널 호출부 식별자 수정 완료."
fi

# 3. 코드 구문 검증 (컴파일 테스트)
echo "[+] 코드 안정성 및 문법 재검증을 진행합니다..."
python -m py_compile *.py

if [ $? -eq 0 ]; then
    echo "[+] [성공] 문법 오류가 완전히 해결되었으며 컴파일에 성공했습니다!"
    echo "[+] GitHub 원격 저장소(`main` 브랜치)로 최종 동기화를 집행합니다."
    
    git config --global user.email "k01057699820@gmail.com"
    git config --global user.name "ryujinchoi"
    
    git add .
    git commit -m "Fix: Resolve Python syntax error in class naming and ensure clean compile"
    git push origin main
    echo "[+] [최종 업데이트 완료] 모든 논리 보완본이 정상적으로 깃허브에 반영되었습니다."
else
    echo "[-] [실패] 아직 파일 내에 다른 문법 오류가 남아있습니다. 코드를 다시 확인해 주세요."
fi
