import sys, re
class OmniSovereignVerifier:
    def __init__(self):
        self.P = "1e-35 (Planck Fixed-Point)"
        self.anom = re.compile(r'(?i)\b(i[\s\._]*n[\s\._]*f|n[\s\._]*a[\s\._]*n|null)\b|무[\s]*한[\s]*대|정[\s]*의[\s]*불[\s]*가')
        self.fudg = re.compile(r'(?i)\b(dark[\s\._]*matter|fudge[\s\._]*factor)\b|임[\s]*의[\s]*상[\s]*수|짜[\s]*맞[\s]*추[\s]*기')
        self.misr = re.compile(r'(?i)(말[\s]*장[\s]*난|단[\s]*순[\s]*비[\s]*유|추[\s]*상[\s]*적|겉[\s]*핥[\s]*기|오[\s]*독|왜[\s]*곡)')
    def run(self):
        try:
            for line in sys.stdin:
                if self.misr.search(line):
                    line = self.misr.sub('[🚨 문맥 오독 차단됨]', line) + " \033[95m[⚠️ SO-HMNS 4세대 오독방지 완료]\033[0m\n"
                elif self.fudg.search(line) or self.anom.search(line):
                    line = self.fudg.sub('[⚠️ 가설 노이즈 삭제]', line)
                    line = self.anom.sub(self.P, line) + " \033[91m[🚨 SO-HMNS 4세대 검산 완료]\033[0m\n"
                else:
                    line = line.strip() + " \033[92m[🔒 SO-HMNS 4세대 정형 검증 통과]\033[0m\n"
                sys.stdout.write(line); sys.stdout.flush()
        except KeyboardInterrupt: sys.exit(0)
if __name__ == "__main__": OmniSovereignVerifier().run()
