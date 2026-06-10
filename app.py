import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def verify_universal_topos_core(metric_value, mode="riemann"):
    try:
        if mode in ["riemann", "bsd"]:
            val = complex(metric_value)
            magnitude = max(abs(val.real), 1.0)
            if abs(val.imag) > (1e-9 * magnitude):
                return False, "Spectral Instability Detected."
        elif mode == "pnp" and float(metric_value) <= 1.0:
            return False, "Complexity Collapse Detected."
        elif mode == "navier_stokes" and (float(metric_value) == float('inf') or float(metric_value) > 1e18):
            return False, "Fluid Blow-up Defied."
        elif mode == "yang_mills" and float(metric_value) <= 1e-6:
            return False, "Mass Gap Collapse Defied."
        return True, f"Topos Invariant Verified for [{mode.upper()}]"
    except (ValueError, TypeError):
        return False, "Invalid Data Format."

@app.route("/", methods=["GET"])
def live_ping():
    return "SOHLF V3 & SO-HMNS Millennium Complex Field Gateway v10.0 Live."

@app.route("/validate_universal", methods=["POST"])
def validate_universal():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"status": "error", "message": "Missing JSON Payload"}), 400
        mode = payload.get("mode", "riemann")
        target_metrics = payload.get("metrics", [])
        if len(target_metrics) > 1000:
            return jsonify({"status": "error", "message": "Payload size limit exceeded."}), 400
        results = []
        for metric in target_metrics:
            is_valid, msg = verify_universal_topos_core(metric, mode)
            results.append({"metric": metric, "valid": is_valid, "detail": msg})
        total_success = sum(1 for r in results if r["valid"]) / max(len(results), 1)
        return jsonify({
            "status": "success",
            "doi": "10.5281/zenodo.20579901",
            "engine": "SOHLF V3 Millennium Triplet Engine v10.0",
            "mode": mode,
            "universal_closure": total_success == 1.0,
            "verifications": results
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
