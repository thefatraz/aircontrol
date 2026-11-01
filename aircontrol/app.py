
from flask import Flask, render_template, request, jsonify
import re
import unicodedata

app = Flask(__name__)

# Trang thai may lanh (ban mo phong)
ac_status = {
    "power": False,
    "temperature": 26,
    "mode": "cool",
    "fan_speed": "auto"
}


def normalize_text(text):
    """Chuyen tieng Viet ve dang khong dau de de nhan dien."""
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        char for char in text
        if unicodedata.category(char) != "Mn"
    )
    return text.replace("đ", "d")


def process_command(command):
    global ac_status

    text = normalize_text(command)
    messages = []

    # Bat may lanh
    if any(word in text for word in [
        "bat may lanh", "mo may lanh", "bat dieu hoa",
        "mo dieu hoa", "turn on"
    ]):
        ac_status["power"] = True
        messages.append("Da bat may lanh.")

    # Tat may lanh
    elif any(word in text for word in [
        "tat may lanh", "tat dieu hoa", "turn off"
    ]):
        ac_status["power"] = False
        messages.append("Da tat may lanh.")

    # Dieu chinh nhiet do
    temperature = re.search(r"(\d{2})\s*(do|độ)", text)

    if temperature:
        value = int(temperature.group(1))

        if 16 <= value <= 30:
            ac_status["temperature"] = value
            messages.append(
                f"Da chinh nhiet do thanh {value} do C."
            )
        else:
            messages.append("Nhiet do phai tu 16 den 30 do C.")

    # Chon che do
    if "hut am" in text or "dry" in text:
        ac_status["mode"] = "dry"
        messages.append("Da chuyen sang che do hut am.")

    elif "quat" in text and "che do quat" in text:
        ac_status["mode"] = "fan"
        messages.append("Da chuyen sang che do quat.")

    elif "lam lanh" in text or "cool" in text:
        ac_status["mode"] = "cool"
        messages.append("Da chuyen sang che do lam lanh.")

    # Toc do quat
    if "quat manh" in text:
        ac_status["fan_speed"] = "high"
        messages.append("Da chinh quat manh.")

    elif "quat nhe" in text:
        ac_status["fan_speed"] = "low"
        messages.append("Da chinh quat nhe.")

    elif "quat tu dong" in text:
        ac_status["fan_speed"] = "auto"
        messages.append("Da chinh quat tu dong.")

    if not messages:
        messages.append(
            "Toi chua hieu lenh. "
            "Hay thu: Bat may lanh, Tat may lanh, "
            "Tang nhiet do len 25 do."
        )

    return {
        "success": True,
        "message": " ".join(messages),
        "status": ac_status
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    user_command = data.get("command", "")

    if not user_command.strip():
        return jsonify({
            "success": False,
            "message": "Ban chua nhap lenh."
        }), 400

    result = process_command(user_command)
    return jsonify(result)


@app.route("/status", methods=["GET"])
def status():
    return jsonify(ac_status)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
