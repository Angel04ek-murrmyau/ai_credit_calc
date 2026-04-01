from flask import Blueprint, render_template, request
from .risk import calculate_risk
from .ai import get_ai_comment
from .db import save_client

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.to_dict()

        risk_score = calculate_risk(data)
        decision = "Одобрено" if risk_score >= 0.5 else "Отказ"

        ai_comment = get_ai_comment(data, risk_score)

        save_client(data, risk_score, decision, ai_comment)

        return render_template(
            "result.html",
            risk=risk_score,
            decision=decision,
            comment=ai_comment
        )

    # 👉 GET-запрос — просто отдать форму
    return render_template("index.html")