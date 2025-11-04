def normalize(v, mn, mx):
    if mx == mn:
        return 0.0
    return max(0.0, min(1.0, (v - mn) / (mx - mn)))

def compute_score(item):
    # item has views, favorites, orders, novelty(0/1)
    weights = {"views": 0.35, "favorites": 0.25, "orders": 0.25, "novelty": 0.15}
    s = 0
    s += weights["views"] * normalize(item.get("views", 0), 0, 10000)
    s += weights["favorites"] * normalize(item.get("favorites", 0), 0, 2000)
    s += weights["orders"] * normalize(item.get("orders", 0), 0, 500)
    s += weights["novelty"] * (1.0 if item.get("novelty", 0) else 0.0)
    return round(s, 4)
