def age_score(age):
    age = int(age)
    if age < 18:
        return 0
    elif age <= 21:
        return 0.2
    elif age <= 30:
        return 0.6
    elif age <= 50:
        return 1.0
    elif age <= 65:
        return 0.7
    return 0.3


def calculate_risk(data):
    age_s = age_score(data["age"])

    income = int(data["income"])
    if income < 1000:
        income_s = 0.2
    elif income < 3000:
        income_s = 0.5
    elif income < 6000:
        income_s = 0.8
    else:
        income_s = 1.0

    job_map = {
        "none": 0,
        "temp": 0.3,
        "part": 0.5,
        "official": 0.8,
        "stable": 1.0
    }
    job_s = job_map.get(data["job"], 0)

    exp = int(data["job_exp"])
    if exp < 6:
        exp_s = 0.2
    elif exp < 12:
        exp_s = 0.4
    elif exp < 36:
        exp_s = 0.7
    else:
        exp_s = 1.0

    loans = int(data["loans"])
    load_ratio = loans / max(income, 1)

    if load_ratio > 0.5:
        load_s = 0.1
    elif load_ratio > 0.3:
        load_s = 0.4
    elif load_ratio > 0.1:
        load_s = 0.7
    else:
        load_s = 1.0

    marital_map = {
        "single": 0.5,
        "married": 0.8,
        "divorced": 0.6
    }
    marital_s = marital_map.get(data["status"], 0.5)

    risk = (
        0.2 * age_s +
        0.2 * income_s +
        0.15 * job_s +
        0.15 * exp_s +
        0.2 * load_s +
        0.1 * marital_s
    )

    return round(risk, 2)