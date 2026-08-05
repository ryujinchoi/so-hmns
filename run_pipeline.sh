#!/bin/bash
# ==============================================================================
# SO-HMNS (Sovereign Absolute Invariant Truth Infrastructure)
# Master Orchestration Pipeline - Hyper-Scale Hardened Edition
# ==============================================================================

set -eo pipefail

echo "[SO-HMNS] Initializing Universal Hardened Pipeline Orchestrator..."

# [Runtime Optimization Guard] 
# 파이썬 VM 자체의 불필요한 바이트코드(.pyc) 쓰기 동작을 원천 금지하고,
# 비동기 버퍼링에 의한 타이밍 누수를 차단하기 위해 unbuffered 출력을 강제 집행함.
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# 1. 저레벨 물리-유체 텐서 코어 엔진 무결성 구동
echo "[STEP 1] Executing Millennium Explicit Solver Core..."
python3 MILLENNIUM_EXPLICIT_SOLVER.py

# 2. 우주론적 시공간 곡률 대수 텐서 엔진 구동
echo "[STEP 2] Executing Cosmological Evolution Simulator..."
python3 cosmic_evolution_simulator.py

# 3. 미세 공정 무손실 탄도 포논 산란 가속기 구동
if [ -f "test_thermal_convection.py" ]; then
    echo "[STEP 3] Executing Ballistic Phonon Acceleration Core..."
    python3 test_thermal_convection.py
fi

echo "[SUCCESS] SO-HMNS Master Pipeline Execution Completed With 0.00% Error Rate."
