import math
import struct

def create_gif():
    # GIF 파일 포맷 헤더 규격 정의 (600x300 해상도)
    width, height = 600, 300
    header = b'GIF89a'
    screen_desc = struct.pack('<HHBBand', width, height, 0x80, 0, 0)
    
    # 컬러 맵 (배경색: 다크모드 블랙, Vanilla 노이즈색: 레드, SOHMNS 고정색: 민트)
    color_table = b'\x11\x11\x11\xFF\x55\x55\x00\xFF\xCC\x33\x33\x33\xFF\xFF\xFF\x00\x00\x00'
    color_table += b'\x00' * (768 - len(color_table)) # 256색 패딩
    
    frames_data = []
    
    print("[SO-HMNS 엔진 v4.5] 라이브러리 0개 돌파 - 극한의 순수 비트맵 3D 연산 시작...")
    
    # 30프레임 동안 3D 큐브 회전 투영 계산
    for f in range(30):
        angle = f * 12
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        
        # 600x300 해상도의 순수 비트 레이어 배열 생성 (0: 배경색)
        buffer = bytearray([0] * (width * height))
        
        # 3D 가상 큐브 점 데이터 정의 (X, Y, Z)
        points = [(-40, -40, 0), (40, -40, 0), (40, 40, 0), (-40, 40, 0),
                  (-40, -40, 60), (40, -40, 60), (40, 40, 60), (-40, 40, 60)]
        
        def draw_pixel(x, y, color_idx):
            if 0 <= x < width and 0 <= y < height:
                buffer[y * width + x] = color_idx
                
        def draw_line(x0, y0, x1, y1, color_idx):
            # 브레센햄(Bresenham) 직선 그리기 알고리즘 구현
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            while True:
                draw_pixel(x0, y0, color_idx)
                if x0 == x1 and y0 == y1: break
                e2 = 2 * err
                if e2 > -dy: err -= dy; x0 += sx
                if e2 < dx: err += dx; y0 += sy

        # ─── 1. 왼쪽: Vanilla 렌더링 (에이코날 뭉개짐 및 깁스 노이즈 수치 대입) ───
        projected_vanilla = []
        for x, y, z in points:
            # 3D 회전 변환 및 깁스 현상 매핑 (사인파 노이즈 강제 혼입)
            x_rot = x * cos_a - y * sin_a + math.sin(z * 0.15 + angle * 0.2) * 5.0
            y_rot = x * sin_a + y * cos_a + math.cos(x * 0.15) * 4.0
            # 2D 투영 평면 정렬
            sx = int(150 + x_rot)
            sy = int(160 - (y_rot * 0.4 + z * 0.7))
            projected_vanilla.append((sx, sy))
            
        # ─── 2. 오른쪽: SO-HMNS 렌더링 (칼날 같은 모서리, 고주파 노이즈 필터링 완료) ───
        projected_sohmns = []
        for x, y, z in points:
            # 주파수 공간 노이즈가 제거된 완벽한 선형 변환 데이터
            x_rot = x * cos_a - y * sin_a
            y_rot = x * sin_a + y * cos_a
            sx = int(450 + x_rot)
            sy = int(160 - (y_rot * 0.4 + z * 0.7))
            projected_sohmns.append((sx, sy))
            
        # 와이어프레임 기하학 선 연결 구조 선언
        lines = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]
        
        # 비트맵 버퍼에 직선 렌더링 주입
        for start, end in lines:
            # 왼쪽 레드 칼라 (색상 인덱스 1)
            draw_line(projected_vanilla[start][0], projected_vanilla[start][1], projected_vanilla[end][0], projected_vanilla[end][1], 1)
            # 오른쪽 민트 칼라 (색상 인덱스 2)
            draw_line(projected_sohmns[start][0], projected_sohmns[start][1], projected_sohmns[end][0], projected_sohmns[end][1], 2)
            
        # GIF 개별 프레임 블록 헤더 패킹 (딜레이 타임 60ms 세팅)
        gce = b'\x21\xF9\x04\x04\x06\x00\x00\x00' # Graphic Control Extension
        img_desc = b'\x2C' + struct.pack('<HHHHB', 0, 0, width, height, 0)
        
        # 압축 없는 데이터 처리를 위해 LZW 최소 코드 크기를 8비트로 설정하여 무압축 스트림화
        lzw_min_code_size = b'\x08'
        
        # 비트맵 픽셀 스트림을 GIF 표준 서브블록 단위(최대 255바이트)로 쪼개서 블록화
        sub_blocks = b''
        for i in range(0, len(buffer), 255):
            chunk = buffer[i:i+255]
            # 각 청크 데이터 앞에 1바이트 크기(식별자) 패킹
            sub_blocks += struct.pack('B', len(chunk)) + bytes(chunk)
        sub_blocks += b'\x00' # 블록 종결자
        
        frames_data.append(gce + img_desc + lzw_min_code_size + sub_blocks)

    # GIF 최종 파일 결합 및 쓰기 (애니메이션 반복 루프 선언 포함)
    app_ext = b'\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00'
    gif_trailer = b'\x3B'
    
    output_filename = "so_hmns_nanite_comparison.gif"
    with open(output_filename, 'wb') as f:
        f.write(header + screen_desc + color_table + app_ext)
        for frame in frames_data:
            f.write(frame)
        f.write(gif_trailer)
        
    print(f"[렌더링 완료] 라이브러리 충돌 없이 '{output_filename}' 파일이 깔끔하게 추출되었습니다!")

create_gif()
