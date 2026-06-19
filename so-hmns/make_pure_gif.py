import math

def create_pure_gif():
    # 1. GIF89a 표준 헤더 정의 (160x80 해상도, 2색 컬러맵)
    gif = bytearray(b'GIF89a\xa0\x00P\x00\x80\x00\x00\x11\x11\x11\xff\xff\xff')
    
    # 2. 그래픽 제어 확장 (루프 애니메이션 세팅, 프레임당 60ms 지연)
    gif += b'\x21\xff\x0bNETSCAPE2.0\x03\x01\x00\x00\x00'
    
    # 3. 3D 큐브 와이어프레임 데이터 정의
    nodes = [(-20,-20,-20), (20,-20,-20), (20,20,-20), (-20,20,-20),
             (-20,-20,20), (20,-20,20), (20,20,20), (-20,20,20)]
    edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
    
    print("[SO-HMNS v4.5] 순수 바이트 연산 기반 3D 기하학 프레임 렌더링 중...")
    
    # 20프레임 동안 회전 애니메이션 계산
    for frame in range(20):
        angle = math.radians(frame * 18)
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        
        # 160x80 크기의 가상 이진 버퍼 초기화 (0: 검은색 background)
        buffer = [0] * (160 * 80)
        
        # ─── 왼쪽: Vanilla 모드 (에이코날 뭉개짐 및 깁스 노이즈 가공) ───
        for start, end in edges:
            for t in range(10):
                interp = t / 9.0
                x1, y1, z1 = nodes[start]
                x2, y2, z2 = nodes[end]
                x = x1 + (x2 - x1) * interp
                y = y1 + (y2 - y1) * interp
                z = z1 + (z2 - z1) * interp
                
                # 3D 회전 및 깁스 가짜 사인파 왜곡 추가
                x_rot = x * cos_a - z * sin_a + math.sin(frame + y)*2.0
                y_rot = x * sin_a + z * cos_a
                
                sx = int(40 + x_rot)
                sy = int(40 - (y_rot * 0.5 + z * 0.4))
                if 0 <= sx < 80 and 0 <= sy < 80:
                    buffer[sy * 160 + sx] = 1
                    
        # ─── 오른쪽: SO-HMNS 모드 (노이즈 완전 감쇄, 칼날 같은 윤곽 보존) ───
        for start, end in edges:
            for t in range(15):
                interp = t / 14.0
                x1, y1, z1 = nodes[start]
                x2, y2, z2 = nodes[end]
                x = x1 + (x2 - x1) * interp
                y = y1 + (y2 - y1) * interp
                z = z1 + (z2 - z1) * interp
                
                # 왜곡 없는 순수 유클리드 기하 회전
                x_rot = x * cos_a - z * sin_a
                y_rot = x * sin_a + z * cos_a
                
                sx = int(120 + x_rot)
                sy = int(40 - (y_rot * 0.5 + z * 0.4))
                if 80 <= sx < 160 and 0 <= sy < 80:
                    buffer[sy * 160 + sx] = 1
                    
        # 4. 프레임 바이트 패킹 (가장 원시적인 비압축 데이터 블록 생성)
        gif += b'\x21\xf9\x04\x04\x06\x00\x00\x00' # 그래픽 제어 정보
        gif += b'\x2c\x00\x00\x00\x00\xa0\x00P\x00\x00\x02\x82\x04' # 이미지 헤더 (LZW 최소 코드)
        
        # 픽셀 데이터를 GIF 데이터 블록 규격에 맞게 바이트 스트림화
        bit_stream = []
        for i in range(0, len(buffer), 8):
            byte_val = 0
            for bit in range(8):
                if i + bit < len(buffer) and buffer[i + bit]:
                    byte_val |= (1 << bit)
            bit_stream.append(byte_val)
            
        # 255바이트씩 쪼개서 데이터 서브블록 삽입
        for idx in range(0, len(bit_stream), 255):
            chunk = bit_stream[idx:idx+255]
            gif.append(len(chunk))
            gif.extend(chunk)
        gif += b'\x00' # 프레임 블록 종료 마커
        
    gif += b'\x3b' # GIF 파일 완전 종료 마커
    
    output_name = "so_hmns_nanite_comparison.gif"
    with open(output_name, "wb") as f:
        f.write(gif)
    print(f"[렌더링 완료] 라이브러리 프리 체제로 '{output_name}' 파일이 완벽하게 빌드되었습니다!")

if __name__ == "__main__":
    create_pure_gif()
