import re
import pdfkit
from pylatexenc.latex2text import LatexNodes2Text

def render_math_to_pdf(tex_file_path, pdf_file_path):
    print("=== [SOHLF V3] Parsing proof.tex Topological Node ===")
    with open(tex_file_path, "r", encoding="utf-8") as f:
        tex_content = f.read()
    
    # 본문 및 초록 데이터 가공 추출
    abstract = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', tex_content, re.DOTALL).group(1).strip()
    intro = re.search(r'\\section{Introduction and Mathematical Preliminaries}(.*?)\\section', tex_content, re.DOTALL).group(1).strip()
    spectral_bound = re.search(r'\\section{Infinite-Dimensional Spectral Filtering and Truncation Bound}(.*?)\\section', tex_content, re.DOTALL).group(1).strip()
    resolution = re.search(r'\\section{Resolution of the Truncation Logical Gap}(.*?)\\end{document}', tex_content, re.DOTALL).group(1).strip()

    # MathJax CDN 스트림을 주입한 초경량 고해상도 HTML 템플릿 빌드 (512MB RAM 오버헤드 0%)
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://polyfill.io"></script>
        <script id="MathJax-script" async src="https://jsdelivr.net"></script>
        <style>
            body {{ font-family: 'Times New Roman', serif; line-height: 1.6; margin: 40px; color: #111; }}
            h1, h2 {{ text-align: center; color: #000; }}
            .metadata {{ text-align: center; font-style: italic; margin-bottom: 30px; }}
            .abstract {{ border: 1px solid #ccc; padding: 15px; margin: 20px 0; background: #fafafa; font-size: 0.95em; }}
            .formula {{ margin: 20px 0; text-align: center; }}
        </style>
    </head>
    <body>
        <h1>Infinite-Dimensional Spectral Operator Bounds for Hallucination-Free Optimization Engines</h1>
        <div class="metadata">Author: ryujinchoi<br>Zenodo DOI Archived: 10.5281/zenodo.20579901</div>
        
        <div class="abstract"><strong>Abstract —</strong> {abstract}</div>
        
        <h2>1. Introduction and Mathematical Preliminaries</h2>
        <p>{intro}</p>
        
        <h2>2. Infinite-Dimensional Spectral Filtering and Truncation Bound</h2>
        <p>{spectral_bound}</p>
        
        <h2>3. Resolution of the Truncation Logical Gap</h2>
        <p>{resolution}</p>
    </body>
    </html>
    """
    
    # 문장 정규화 및 LaTeX 수식 기호 보호 매핑 호환성 정형화
    html_content = html_template.replace(r'\[', '$$').replace(r'\]', '$$')
    html_content = html_content.replace(r'\(', '$').replace(r'\)', '$')

    # Termux 로컬 파일 저장 및 pdfkit 컴파일 트리거
    options = {'quiet': '', 'page-size': 'A4', 'margin-top': '0.75in', 'margin-right': '0.75in', 'margin-bottom': '0.75in', 'margin-left': '0.75in'}
    
    try:
        pdfkit.from_string(html_content, pdf_file_path, options=options)
        print("💡 [SUCCESS] proof.pdf asset successfully compiled via Python Kernel Topology Integration.")
    except Exception as e:
        # wkhtmltopdf 미설치 환경 대비 원시 텍스트 로그 보존 백업 보완 구조 가동
        with open("proof_cleansed.txt", "w", encoding="utf-8") as f_out:
            f_out.write(LatexNodes2Text().latex_to_text(tex_content))
        print("⚠️ pdfkit 종속성 경고: 원문 수식을 구조화된 proof_cleansed.txt 원본 자산으로 실시간 분리 가동 완료.")

if __name__ == "__main__":
    render_math_to_pdf("proof.tex", "proof.pdf")
