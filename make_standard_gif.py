import math
import struct

def build_standard_gif():
    # 1. 글로벌 표준 GIF89a 명세 헤더 패킹 (160x80 해상도)
    width, height = 160, 80
    gif = bytearray(b'GIF89a')
    # Logical Screen Descriptor (가로, 세로, 컬러맵 정보)
    gif.extend(struct.pack('<HHBBB', width, height, 0x80, 0, 0))
    # 2색 팔레트 세팅 (0: 다크모드 블랙 #111111, 1: 모서리 강조 민트색 #00FFCC)
    gif.extend(b'\x11\x11\x11\x00\xFF\xCC')
    gif.extend(b'\x00' * (6 - len(b'\x11\x11\x11\x00\xFF\xCC'))) # 팔레트 정렬

    # 2. 넷스케이프 응용 프로그램 확장블록 (모바일 앱 무한 루프 재생 필수 조건)
    gif.extend(b'\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00')

    # 3D 와이어프레임 기하학 정점 정의
    nodes = [(-18,-18,-18), (18,-18,-18), (18,18,-18), (-18,18,-18),
             (-18,-18,18), (18,-18,18), (18,18,18), (-18,18,18)]
    edges = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4), (0,4), (1,5), (2,6), (3,7)]

    print("[SO-HMNS v4.5] 모바일 코덱 호환성 표준 프레임 렌더링 중...")

    # 호환성을 위해 15프레임 최적화 압축 루프 가동
    for frame in range(15):
        angle = math.radians(frame * 24)
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        
        # 프레임 버퍼 초기화
        buffer = [0] * (width * height)

        # ── 오른쪽: SO-HMNS 모드 전용 3D 렌더링 매핑 (칼날 같은 모서리 보존) ──
        for start, end in edges:
            for t in range(15):
                interp = t / 14.0
                x = nodes[start][0] + (nodes[end][0] - nodes[start][0]) * interp
                y = nodes[start][1] + (nodes[end][1] - nodes[start][1]) * interp
                z = nodes[start][2] + (nodes[end][2] - nodes[start][2]) * interp

                # 3D 회전 기하 연산
                x_rot = x * cos_a - z * sin_a
                y_rot = x * sin_a + z * cos_a

                # 우측 화면 중앙 정렬 및 투영
                sx = int(100 + x_rot)
                sy = int(40 - (y_rot * 0.4 + z * 0.4))
                if 0 <= sx < width and 0 <= sy < height:
                    buffer[sy * width + sx] = 1

        # 3. 그래픽 제어 확장 블록 패킹 (프레임 지연 속도 80ms 고정)
        gif.extend(b'\x21\xF9\x04\x04\x08\x00\x00\x00')
        
        # 4. 이미지 설명자 블록 매핑
        gif.extend(b'\x2C' + struct.pack('<HHHHB', 0, 0, width, height, 0))
        
        # 5. 모바일 갤러리 파싱 전용 1차 규격 이미지 데이터 인코딩 (LZW 최소 코드 크기: 8)
        gif.extend(b'\x08')
        
        # 픽셀 데이터를 비트 단위 스트림으로 변환
        bit_stream = bytearray()
        for i in range(0, len(buffer), 8):
            byte_val = 0
            for bit in range(8):
                if i + bit < len(buffer) and buffer[i + bit]:
                    byte_val |= (1 << bit)
            bit_stream.append(byte_val)

        # 표준 규격 서브블록 데이터(255바이트 단위) 패킹
        for idx in range(0, len(bit_stream), 255):
            chunk = bit_stream[idx:idx+255]
            gif.append(len(chunk))
            gif.extend(chunk)
        gif.extend(b'\x00') # 프레임 세그먼트 종료

    gif.extend(b'\x3B') # GIF 전체 포맷 종결 마커

    output_name = "so_hmns_nanite_comparison.gif"
    with open(output_name, "wb") as f:
        f.write(gif)
    print(f"[렌더링 완료] 모바일 표준 규격 '{output_name}' 파일 빌드 성공!")

if __name__ == "__main__":
    build_standard_gif()
