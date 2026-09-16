def recommended_action(row):
    score = float(row.get("Lead_Score", 0) or 0)
    origin = str(row.get("Lead Origin", "") or "")
    visits = float(row.get("TotalVisits", 0) or 0)
    time_on_site = float(row.get("Total Time Spent on Website", 0) or 0)
    if score >= 80 or (score >= 72 and time_on_site >= 600):
        return "Contact within 15 minutes and route to a senior sales rep."
    if score >= 50 and (visits >= 3 or "Organic" in origin):
        return "Schedule outreach today and add to the active nurture sequence."
    if score >= 50:
        return "Send targeted nurture content and monitor engagement."
    return "Keep lower priority until engagement or firmographic signals improve."


def top_driver(row):
    signals = []
    if float(row.get("Total Time Spent on Website", 0) or 0) > 600:
        signals.append("High time on site")
    if float(row.get("TotalVisits", 0) or 0) >= 5:
        signals.append("Frequent visits")
    origin = row.get("Lead Origin") or row.get("Lead Source")
    if origin:
        signals.append(str(origin))
    occupation = row.get("What is your current occupation")
    if occupation and str(occupation).lower() not in {"unknown", "select", "nan"}:
        signals.append(str(occupation))
    return " + ".join(signals[:2]) if signals else "Model score"
