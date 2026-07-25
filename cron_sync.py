import urllib.request
import json
import datetime

def fetch_and_calculate_seismic():
    url = "https://usgs.gov"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=15)
        data = json.loads(response.read().decode('utf-8'))
        
        alerts = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            geom = feature.get('geometry', {})
            coords = geom.get('coordinates', [0.0, 0.0, 0.0])
            
            # 🔒 [완전 자동 시간 계산] 봇 기동 시각이 아닌, USGS 고유의 Epoch ms 값을 가져와 UTC 표준 포맷으로 자동 변환 연산
            epoch_ms = props.get('time')
            if epoch_ms:
                event_date = datetime.datetime.fromtimestamp(epoch_ms / 1000.0, tz=datetime.timezone.utc)
                formatted_time = event_date.strftime('%Y-%m-%d %H:%M:%S UTC')
            else:
                continue
                
            mag = props.get('mag')
            if mag is not None:
                alerts.append({
                    "mag": str(round(float(mag), 4)),
                    "type": "critical" if float(mag) >= 6.0 else "advisory",
                    "lat": str(round(float(coords[1]), 4)),
                    "lng": str(round(float(coords[0]), 4)),
                    "time": formatted_time, # 자동으로 역산된 고유 발생 시간 바인딩
                    "badge": props.get('place', 'Global Fault Zone Node')
                })
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({"alerts": alerts}, f, indent=4, ensure_ascii=False)
        print("[+] [SO-HMNS] Data pipeline synchronized cleanly with real-time calculated matrices.")
        return True
    except Exception as e:
        print(f"[-] [OFFLINE RETRY] Waiting for network restoration: {str(e)}")
        return False

if __name__ == "__main__":
    fetch_and_calculate_seismic()
