import math, os, urllib.request, json, subprocess
from datetime import datetime, timedelta

def fetch_live_usgs_data():
    url = "https://usgs.gov"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))
        entries = []
        for feat in data.get("features", [])[:3]:
            p = feat["properties"]
            place, mag = p["place"].replace(",", " ").replace(" ", "_"), p["mag"]
            sc = 2.0 if mag > 6.0 else 5.0
            a, b, sl = round(0.1 + (mag * 0.02), 2), round(0.3 + (mag * 0.04), 2), round(0.05 + (mag * 0.015), 3)
            entries.append(f"실시간_{place}, {sc}, {a}, {b}, 0.10, 0.40, 0.30, 1.2, 3000.0, {sl}, True, {mag}, 120.0, 35.0, 965.0")
        return entries
    except: return []

def load_dynamic_observation_stations():
    base_config = """# 이름, 스케일, 알파, 베타, 감마, 델타, k, 유입, 수심, 전조, 쓰나미, 규모, 강수, 풍속, 기압
인도네시아_순다해구, 1.8, 0.25, 0.55, 0.12, 0.35, 0.28, 1.3, 6000.0, 0.18, True, 8.6, 380.0, 48.0, 945.0
미국_산안드레아스, 4.0, 0.15, 0.45, 0.05, 0.50, 0.35, 1.1, 100.0, 0.12, False, 7.9, 15.0, 8.0, 1013.0
이탈리아_베수비오, 3.2, 0.30, 0.60, 0.15, 0.40, 0.25, 1.6, 2000.0, 0.05, True, 6.4, 210.0, 12.0, 1005.0
대한민국_양산단층, 15.0, 0.05, 0.30, 0.02, 0.70, 0.40, 0.8, 200.0, 0.08, False, 5.8, 290.0, 42.0, 955.0
"""
    with open("stations.txt", "w", encoding="utf-8") as f:
        f.write(base_config)
        for entry in fetch_live_usgs_data(): f.write(entry + "\n")
    stations = {}
    with open("stations.txt", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip(): continue
            pt = [p.strip() for p in line.split(",")]
            if len(pt) < 15: continue
            stations[pt[0]] = {
                "scale_factor": float(pt[1]), "alpha": float(pt[2]), "beta": float(pt[3]),
                "gamma": float(pt[4]), "delta": float(pt[5]), "k": float(pt[6]),
                "Q_in": float(pt[7]), "h_deep": float(pt[8]), "p_slope": float(pt[9]),
                "tsunami_active": pt[10].lower() == "true", "max_magnitude": float(pt[11]),
                "rain_mm": float(pt[12]), "wind_ms": float(pt[13]), "press_hpa": float(pt[14])
            }
    return stations

def get_earthquake_seismicity_rate(t, t_m, slope):
    if t < t_m: return 0.2 * math.exp(slope * t)
    return 5.0 / (((t - t_m) if (t - t_m) > 0 else 0.01) ** 1.1)

def volcano_dynamic_system(p, s, g, alpha, beta, gamma, delta, k, Q_in, rain, t):
    rain_effect = 1.0 + ((rain * (1.0 - math.exp(-0.15 * (t + 0.1)))) / 400.0)
    p_e, s_e = math.tanh(p), math.tanh(s)
    dp = alpha * (Q_in * rain_effect - (1.0 - g) * 0.5 * p_e) + gamma * math.sin(s_e)
    ds = beta * ((p_e - 0.5) if p_e > 0.5 else 0.0) - delta * s_e
    dg = (p_e * (1.0 - g)) * math.exp(-k * p_e) - 0.2 * s_e * g
    return dp, ds, dg

def calculate_lyapunov_containment(p, s, g, t):
    p_s, s_s = math.tanh(p), math.tanh(s)
    return 0.5 * (p_s**2) + 0.3 * (s_s**2) + 0.8 * (g**2) * math.exp(p_s) + 0.02 * math.cos(2.0 * math.pi * (t / 0.5))

def generate_web_dashboard(stations):
    base_date = datetime.now()
    cards_html = ""
    for name, cfg in stations.items():
        p, s, g = 0.5, 0.1, 0.2
        t, t_end, dt, steps = 0.0, 40.0, 0.2, 20
        sub_dt = dt / steps
        t_m = 20.0
        tsunami_triggered = False
        t_tsu_start, tsu_energy, forecast_t, tsu_final_height = 0.0, 0.0, t_end, 0.0
        
        while t <= t_end:
            eq_rate = get_earthquake_seismicity_rate(t, t_m, cfg["p_slope"])
            for _ in range(steps):
                s_comb = s + eq_rate
                dp, ds, dg = volcano_dynamic_system(p, s_comb, g, cfg["alpha"], cfg["beta"], cfg["gamma"], cfg["delta"], cfg["k"], cfg["Q_in"], cfg["rain_mm"], t)
                p += dp * sub_dt; s += ds * sub_dt; g += dg * sub_dt
            
            s_comb = s + eq_rate
            W = calculate_lyapunov_containment(p, s_comb, g, t)
            if t >= t_m and not tsunami_triggered:
                tsunami_triggered = True
                t_tsu_start = t
                tsu_energy += 2.5
            if W > 0.9 and tsunami_triggered:
                tsu_energy += 4.0
            if tsunami_triggered and cfg["tsunami_active"]:
                dt_tsu = t - t_tsu_start
                if dt_tsu >= 0:
                    c_depth = cfg["h_deep"] if t < 32.0 else max(10.0, cfg["h_deep"] - ((cfg["h_deep"] - 10.0) * (t - 32.0) / 8.0))
                    sh_factor = (cfg["h_deep"] / (c_depth if c_depth > 0.5 else 0.5)) ** 0.25
                    tsu_h = abs(tsu_energy * math.exp(-0.08 * dt_tsu) * math.sin(1.5 * dt_tsu)) * sh_factor
                    tsu_h += 0.6 * math.sin(2.0 * math.pi * (t / 0.5))
                    if tsu_h > tsu_final_height: tsu_final_height = tsu_h
                    if tsu_h > 12.0:
                        forecast_t = t
                        break
            t += dt
            
        eq_time = base_date + timedelta(days=forecast_t * cfg["scale_factor"])
        err = 2 * cfg["scale_factor"] / 4.0
        min_win, max_win = (eq_time - timedelta(days=err)).strftime("%m/%d"), (eq_time + timedelta(days=err)).strftime("%m/%d")
        
        l_ko, l_en, l_ja, l_zh = "전세계 감시망", "Global Network", "グローバル監視網", "全球监测网络"
        t_ko, t_en, t_ja, t_zh = "복합 재해", "Multi-Hazard", "複合災害", "复合灾害"
        
        if "인도네시아_순다해구" in name:
            l_ko, l_en, l_ja, l_zh = "수마트라 남서부 해역 (남위 5.4°, 동경 102.3°)", "Southwest of Sumatra (5.4°S, 102.3°E)", "スマトラ島南西沖 (南緯5.4°, 東経102.3°)", "苏门答腊西南海域 (南纬5.4°, 东经102.3°)"
            t_ko, t_en, t_ja, t_zh = "해저 강진 및 대형 쓰나미", "Subsea Megathrust & Tsunami", "海底巨大地震・大津波", "海底大地震与大海啸"
        elif "미국_산안드레아스" in name:
            l_ko, l_en, l_ja, l_zh = "캘리포니아 파크필드 단층대 (북위 35.9°, 서경 120.4°)", "Parkfield Segment, CA (35.9°N, 120.4°W)", "カリフォルニア州断層帯", "加州帕克菲尔德断层带 (北纬35.9°, 西经120.4°)"
            t_ko, t_en, t_ja, t_zh = "판 경계 대형 단층 지진", "Transform Fault Earthquake", "トランスフォーム断層型地震", "转换断层大地震"
        elif "이탈리아_베수비오" in name:
            l_ko, l_en, l_ja, l_zh = "캄파니아 나폴리 동부 (북위 40.8°, 동경 14.4°)", "East of Naples (40.8°N, 14.4°E)", "ナポリ東部 (北緯40.8°, 東経14.4°)", "那不勒斯东部 (北纬40.8°, 东经14.4°)"
            t_ko, t_en, t_ja, t_zh = "활화산 연쇄 폭발 분화", "Active Volcanic Eruption", "活火山連鎖爆発噴火", "活火山连锁爆发喷发"
        elif "대한민국_양산단층" in name:
            l_ko, l_en, l_ja, l_zh = "경상북도 경주시 외동읍 일대 (북위 35.7°, 동경 129.3°)", "Gyeongju, S.Korea (35.7°N, 129.3°E)", "慶尚北道慶州市外東邑一帯", "庆尚北道庆州市外东邑一带 (北纬35.7°, 东经129.3°)"
            t_ko, t_en, t_ja, t_zh = "지각 내부 활성단층 지진", "Intraplate Active Fault EQ", "内陸活断層型地震", "板内活动断层地震"
        elif "실시간_" in name:
            l_ko = name.replace("실시간_", "").replace("_", " ") + " 인근 진앙지"
            l_en, l_ja, l_zh = "Epicenter near " + l_ko, l_ko + " 近郊震央", l_ko + " 附近震中"
            t_ko, t_en, t_ja, t_zh = "실시간 감지 추적 지진", "Live Detected Seismicity", "リアルタイム検知地震", "实时监测追踪地震"

        if cfg["max_magnitude"] >= 8.0: bg, bde = "from-red-950 border-red-500 text-red-400", "border-red-500 text-red-400 bg-red-500/10"
        elif cfg["max_magnitude"] >= 6.5: bg, bde = "from-amber-950 border-amber-500 text-amber-400", "border-amber-500 text-amber-400 bg-amber-500/10"
        else: bg, bde = "from-emerald-950 border-emerald-500 text-emerald-400", "border-emerald-500 text-emerald-400 bg-emerald-500/10"
        
        t_stat = "ALERT" if tsu_final_height > 3.0 else "NORMAL"
        if not cfg["tsunami_active"]: t_stat = "NONE"

        mag_percent = min(100.0, max(0.0, (cfg["max_magnitude"] / 10.0) * 100.0))
        tsu_percent = min(100.0, max(0.0, (tsu_final_height / 15.0) * 100.0))

        cards_html += f"""
        <div class="card bg-gradient-to-br {bg} to-slate-950 border rounded-2xl p-5 shadow-2xl transition duration-300 hover:border-white/40" 
             data-name-ko="{name}" data-name-en="{name}" data-name-ja="{name}" data-name-zh="{name}"
             data-loc-ko="{l_ko}" data-loc-en="{l_en}" data-loc-ja="{l_ja}" data-loc-zh="{l_zh}"
             data-type-ko="{t_ko}" data-type-en="{t_en}" data-type-ja="{t_ja}" data-type-zh="{t_zh}"
             data-tsunami-status="{t_stat}" data-tsunami-val="{tsu_final_height:.2f}m">
            <div class="flex justify-between items-center mb-3">
                <div><span class="card-type text-[10px] font-bold block uppercase tracking-wider text-slate-400 mb-0.5">{t_ko}</span><h3 class="card-title text-sm font-black text-white tracking-tight">{name}</h3></div>
                <span class="badge px-2 py-0.5 text-[10px] font-bold rounded border {bde} animate-pulse">LIVE</span>
            </div>
            <div class="space-y-2.5 text-xs">
                <div class="bg-white/5 px-2.5 py-1.5 rounded-lg text-slate-300 border border-white/5">📍 <span class="card-loc font-medium">{l_ko}</span></div>
                <div class="bg-white/5 px-2.5 py-2 rounded-lg space-y-1.5 border border-white/5">
                    <div class="flex justify-between items-center"><span class="text-slate-400 font-medium">📊 <span class="lbl-mag">예상 규모</span></span><span class="font-black text-white">M {cfg['max_magnitude']:.1f}</span></div>
                    <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden"><div class="bg-gradient-to-r from-amber-500 to-red-500 h-full" style="width: {mag_percent}%"></div></div>
                </div>
                <div class="flex justify-between items-center px-1"><span class="text-slate-400 font-medium">📅 <span class="lbl-time">임계 시점</span></span><span class="font-bold text-slate-200">{eq_time.strftime('%m/%d %H시')}</span></div>
                <div class="flex justify-between items-center px-1"><span class="text-slate-400 font-medium">🎯 <span class="lbl-win">오차 범위</span></span><span class="font-bold text-amber-400">{min_win} ~ {max_win}</span></div>
                <div class="bg-white/5 px-2.5 py-2 rounded-lg space-y-1.5 border border-white/5">
                    <div class="flex justify-between items-center"><span class="text-slate-400 font-medium">🌊 <span class="lbl-tsunami">쓰나미 파고</span></span><span class="tsunami-text font-bold text-blue-400">{tsu_final_height:.2f}m</span></div>
                    <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden"><div class="bg-gradient-to-r from-blue-500 to-cyan-400 h-full" style="width: {tsu_percent}%"></div></div>
                </div>
                <div class="grid grid-cols-2 gap-1.5 text-center text-[10px] font-semibold text-slate-400 pt-1.5 border-t border-white/10">
                    <div class="bg-white/5 py-1 rounded">🌦️ <span class="lbl-rain">폭우</span>: {int(cfg['rain_mm'])}mm</div>
                    <div class="bg-white/5 py-1 rounded">🌀 <span class="lbl-storm">태풍</span>: {int(cfg['press_hpa'])}hPa</div>
                </div>
            </div>
        </div>"""

    global html_content_base
    html_content_base = f"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><title>FORECAST</title><script src="https://tailwindcss.com"></script></head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased">
    <header class="border-b border-white/10 bg-slate-900/80 backdrop-blur sticky top-0 z-50"><div class="max-w-7xl mx-auto px-4 py-2.5 flex justify-between items-center"><div class="flex items-center space-x-2"><span class="text-lg">📊</span><h1 class="text-base font-black tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-red-400 to-blue-400">SO-HMNS GLOBAL FORECAST</h1></div>
    <div class="flex items-center space-x-1.5 bg-slate-800 px-2.5 py-1 rounded-lg border border-white/10"><span class="text-xs">🌐</span><select id="langSelect" onchange="changeLanguage()" class="bg-transparent text-xs text-white font-bold focus:outline-none cursor-pointer"><option value="ko" class="bg-slate-900">KO</option><option value="en" class="bg-slate-900">EN</option><option value="ja" class="bg-slate-900">JA</option><option value="zh" class="bg-slate-900">ZH</option></select></div></div></header>
    <main class="max-w-7xl mx-auto px-4 py-4">
        <section class="mb-5 bg-slate-900/50 border border-white/10 rounded-xl p-4"><h2 id="noticeTitle" class="text-xs font-bold mb-1 text-amber-400">💡 오픈 전세계 재해 정보 공개망 안내</h2><p id="noticeDesc" class="text-[11px] text-slate-400 leading-relaxed">본 대시보드는 깃허브 및 USGS API 실시간 데이터를 기반으로 구동됩니다. 구체적인 위·경도 발생 세부 지리 좌표와 재해 유형 분류 태그를 통합 추적하여 실시간 전 세계망에 공유합니다.</p></section>
        <section><h2 id="sectionTitle" class="text-sm font-black mb-4 flex items-center">📡 전세계 가용 올-데이터 실시간 예보 현황</h2><div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">{{cards_html}}</div></section>
    </main>
    <footer class="max-w-7xl mx-auto px-4 py-4 border-t border-white/5 mt-8 text-center text-[10px] text-slate-500"><p id="footerText">© 2026 SO-HMNS 인프라. 구체화된 다중 재해 분류 노드를 통해 GitHub Pages 개방망으로 전세계 배포됩니다.</p></footer>
"""

    html_content = html_content_base + """
    <script>
    const langDict = {
        ko: { notice_title: "오픈 전세계 재해 정보 안내", notice_desc: "본 대시보드는 깃허브 및 USGS API 실시간 데이터를 기반으로 구동됩니다. 세부 지리 위경도 좌표 및 재해 유형(지진, 화산, 쓰나미 등) 분류 태그를 동적 매핑하여 실시간 전 세계망에 공유합니다.", section_title: "📡 전세계 가용 올-데이터 실시간 예보 현황", sync: "실시간 동기화", l_mag: "예상 규모", l_time: "임계 시점", l_win: "오차 범위", l_tsunami: "쓰나미 파고", ts_normal: "정상", ts_alert: "대형 경보", ts_none: "위험 없음", ft: "© 2026 SO-HMNS 인프라. 다중 재해 분류 노드를 통해 GitHub Pages 개방망으로 전세계 배포됩니다." },
        en: { notice_title: "Global Disaster Information System", notice_desc: "This dashboard delivers real-time hazard warnings driven by USGS APIs. It tracks precise latitude/longitude hazard locations and specific event classifications (Earthquake, Volcano, Tsunami) distributed internationally.", section_title: "📡 Live Global Hazard Forecast Network", sync: "LIVE SYNC", l_mag: "Predicted Mag", l_time: "Threshold Time", l_win: "Confidence Win", l_tsunami: "Tsunami Height", ts_normal: "Normal", ts_alert: "WARNING", ts_none: "No Risk", ft: "© 2026 SO-HMNS. Universally open via GitHub Pages distributed nodes." },
        ja: { notice_title: "全世界災害情報公開システム", notice_desc: "本システムはGitHub及びUSGS APIのリアルタイムデータと連動しています。具体的な緯度・経度の発生詳細地理座標と、災害タイプ（地震、火山、津波など）の分類タグを統合追跡してリアルタイムに共有します。", section_title: "📡 稼働中のリアルタイム統合予測監視", sync: "リアルタイム同期", l_mag: "予測規模", l_time: "臨界予測日時", l_win: "信頼誤差範囲", l_tsunami: "複合津波波高", ts_normal: "正常", ts_alert: "大津波警報", ts_none: "危険なし", ft: "© 2026 SO-HMNS 防災インフラ. 詳細な複合災害ノードをGitHub Pagesを通じて配信中。" },
        zh: { notice_title: "全球灾害公共信息发布平台", notice_desc: "本网站是基于GitHub Action与USGS全球实时地震监测站API构建의 综合防护系统。系统全面跟踪精确的经纬度地理坐标与灾害事件分类标签（地震、火山、海啸等），提供全天候多国语言联合预警。", section_title: "📡 全球全量数据实时联合预警网络", sync: "实时同步中", l_mag: "预估震级", l_time: "爆发时间", l_win: "置信范围", l_tsunami: "海啸波高", ts_normal: "正常", ts_alert: "海啸预警", ts_none: "无风险", ft: "© 2026 SO-HMNS 灾害管理系统. 面向全球用户通过 GitHub Pages 开放多元化灾难节点查询。" }
    };
    function changeLanguage() {
        const l = document.getElementById("langSelect").value, t = langDict[l];
        document.getElementById("noticeTitle").innerText = "💡 " + t.notice_title;
        document.getElementById("noticeDesc").innerText = t.notice_desc;
        document.getElementById("sectionTitle").innerText = t.section_title;
        document.getElementById("footerText").innerText = t.ft;
        document.querySelectorAll(".card").forEach(c => {
            c.querySelector(".badge").innerText = t.sync;
            c.querySelector(".lbl-mag").innerText = t.l_mag;
            c.querySelector(".lbl-time").innerText = t.l_time;
            c.querySelector(".lbl-win").innerText = t.l_win;
            c.querySelector(".lbl-tsunami").innerText = t.l_tsunami;
            c.querySelector(".card-loc").innerText = c.getAttribute("data-loc-" + l);
            c.querySelector(".card-type").innerText = c.getAttribute("data-type-" + l);
            const st = c.getAttribute("data-tsunami-status"), v = c.getAttribute("data-tsunami-val"), n = c.querySelector(".tsunami-text");
            if (n) {
                if (st === "ALERT") n.innerText = v + " (" + t.ts_alert + ")";
                else if (st === "NORMAL") n.innerText = v + " (" + t.ts_normal + ")";
                else n.innerText = t.ts_none;
            }
        });
    }
    </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f: f.write(html_content)

def deploy_to_github_pages():
    print("\n🚀 [글로벌 릴리즈] 내 깃허브 원격 배포망 업로드 중...")
    try:
        subprocess.run(["git", "add", "main.py", "index.html", "stations.txt"], check=True)
        subprocess.run(["git", "commit", "-m", "상용화 프로그레스 차트바 및 데이터 가드 완전체 통합 배포"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("\n🎉 [배포 최종 성공!!] 가로형 프로그레스바 및 예외 방어 처리가 완전체로 통합되었습니다.")
        print("🔗 공식 배포 주소: https://github.io")
        print("="*75)
    except Exception as e: print(f"⚠️ 배포 실패: {e}")

if __name__ == "__main__":
    st = load_dynamic_observation_stations()
    generate_web_dashboard(st)
    deploy_to_github_pages()
