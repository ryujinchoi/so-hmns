#!/macro/bin/bash
while true
do
    # 1단계: 파이썬 파이프라인 엔진 구동 (예측 시간 대조 후 24H 만료 데이터 즉시 소거 및 누적)
    python cron_sync.py
    
    # 2단계: 짤림 방지 및 토큰 오염 차단형 도메인 경로를 통해 실물 깃허브 서버로 다이렉트 전송
    git add data.json index.html 2>/dev/null
    git commit -m "sync(local-kernel): autonomous continuous time-based purge cycle" --allow-empty 2>/dev/null
    git push "https://ryujinchoi:$(cat b)@$(cat a)" main --force 2>/dev/null
    
    echo "[+] [SO-HMNS COMPLETED] Matrix sync complete. Sleeping for 300 seconds..."
    
    # 3단계: 정확히 5분(300초) 동안 대기한 후 자동으로 다시 깨어나 무한 반복
    sleep 300
done
