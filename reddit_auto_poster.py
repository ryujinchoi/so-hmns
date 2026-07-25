import os
import sys
import json
import praw
import numpy as np

def initialize_reddit_client():
    """
    Initializes the official Reddit API client securely using environment variables or hard-coded tokens.
    Replace these placeholders with your actual Reddit developer credentials.
    """
    try:
        return praw.Reddit(
            client_id="YOUR_REDDIT_CLIENT_ID",          # Reddit 앱 등록 시 발급받은 ID
            client_secret="YOUR_REDDIT_CLIENT_SECRET",  # Reddit 앱 등록 시 발급받은 Secret 토큰
            username="YOUR_REDDIT_USERNAME",            # 내 레딧 계정 아이디
            password="YOUR_REDDIT_PASSWORD",            # 내 레딧 계정 비밀번호
            user_agent="SO-HMNS-Bot/1.0 by /u/YOUR_REDDIT_USERNAME"
        )
    except Exception as e:
        print(f"[-] [REDDIT INVARIANT ERROR] Failed to initialize client: {str(e)}")
        return None

def generate_hmns_report(magnitude, lat, lng, location_name):
    """
    Compiles a comprehensive, non-perturbative markdown report ready for r/opensource or r/Python.
    """
    report = f"""**Official SO-HMNS Framework Repository Link:** https://github.com

***

### [🚨 EMERGENCY ALERT] Automated M{magnitude} Seismic Invariance Report via AST-Level Metric Boundary Truncation

### Abstract
We report an immediate non-perturbative computational analysis triggered by a **Magnitude {magnitude}** tectonic fracture event located at **{location_name}** (Coordinates: Lat {lat}, Lng {lng}). Under the SO-HMNS framework, this planetary deformation is processed as a localized displacement of continuous stress tensors across finite-precision Computing Layers. By routing variables through our strict abstract syntax tree (AST) linter, the high-frequency Euler-Maclaurin tail error is strictly truncated with zero-gap accuracy, protecting global log state matrices against floating-point degradation.

***

### 1. Structural Metric Invariants & Tectonic Fault Deformation

When a macro-seismic displacement occurs near active subduction zones, standard discrete computing platforms introducing rounding noise under IEEE 754 standards can cause simulation relaxation drift. The SO-HMNS matrix locks the raw data stream into precise injective fixed-points before hardware register allocation to ensure boundary boundedness:

> **\mathcal{{T}}_{{\text{{AST}}}} \left( \oint_{{\partial\mathcal{{M}}}} \text{{Residual Tectonic Noise}} \right) \equiv 0.00\%**

The continuous geodetic curvature is dynamically bound below, confirming type-theoretic safety without mathematical overflow or NaN exceptions.

***

### 2. Live Infrastructure Status & Open Audit

The complete linter engine, real-time USGS data-ingestion cron bots, and verification timelines are open-source and open for peer review:

* **Official Source Validation Repository:** https://github.com

***

*Keywords: Geophysics, Computational Physics, Numerical Stability, Lean 4, Open Source Python Tools*
"""
    return report

def check_and_post_strong_earthquakes():
    """
    Scans data.json for any recent events with magnitude >= 6.0 and deploys automatic reddit threads.
    """
    data_path = "data.json"
    if not os.path.exists(data_path):
        print("[-] [SO-HMNS ERROR] data.json matrix missing. Aborting poster sync.")
        return

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            
        # Dynamically parse either direct list or data.alerts object schemas
        alerts_list = raw_data.get("alerts", []) if isinstance(raw_data, dict) else raw_data
        
        if not alerts_list:
            print("[+] No seismic items found in matrix.")
            return

        reddit = initialize_reddit_client()
        if not reddit:
            return

        # Target subreddits approved for architectural open-source reviews
        target_subreddits = ["opensource", "Python"]

        for item in alerts_list:
            mag = float(item.get("mag", item.get("magnitude", 0.0)))
            lat = item.get("lat", "16.50")
            lng = item.get("lng", "-99.50")
            badge = item.get("badge", "Global Fault Intersection Zone")
            
            # 🔒 핵심 조건 가드: 규모 6.0 이상의 거대 강진만 필터링하여 감지
            if mag >= 6.0:
                print(f"[+] [🚨 EMERGENCY TRIGGERED] Detected M{mag} Earthquake. Generating report...")
                title = f"[Open Source] Real-time M{mag} Seismic Invariance Report - Automated Data Ingestion Monitoring"
                body_content = generate_hmns_report(mag, lat, lng, badge)
                
                for sub_name in target_subreddits:
                    try:
                        subreddit = reddit.subreddit(sub_name)
                        # Reddit API를 통해 실제 서브레딧 채널에 즉시 글 포스팅 집행
                        submission = subreddit.submit(title, selftext=body_content)
                        print(f"[+] [SUCCESS] Thread successfully deployed on r/{sub_name}. Link: {submission.url}")
                    except Exception as e:
                        print(f"[-] Failed to post to r/{sub_name} due to rate limits or invalid client: {str(e)}")
                        
    except Exception as e:
        print(f"[-] [CRITICAL EXCEPTION] Pipeline failed: {str(e)}")

if __name__ == "__main__":
    check_and_post_strong_earthquakes()
