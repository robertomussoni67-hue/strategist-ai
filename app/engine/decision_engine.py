import json
import os
from typing import Dict, Any, List, Tuple

OPERATORS = {
    ">": lambda a, b: a is not None and a > b,
    "<": lambda a, b: a is not None and a < b,
    ">=": lambda a, b: a is not None and a >= b,
    "<=": lambda a, b: a is not None and a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "in": lambda a, b: a in b if b is not None else False,
    "not_in": lambda a, b: a not in b if b is not None else False,
    "exists": lambda a, b: (a is not None) if b else (a is None),
}

def _scale(x: float, tgt: float, maxv: float) -> float:
    if x is None: return 0.0
    if x <= 0 and tgt > 0: return 0.0
    return max(0.0, min(1.0, x / maxv))

def _scale_inv(x: float, tgt: float, maxv: float) -> float:
    if x is None: return 0.0
    if x <= 0: return 1.0
    val = 1.0 - min(1.0, x / maxv)
    return max(0.0, val)

class DecisionEngine:
    def __init__(self, philosophies_path: str = 'config/philosophies.json'):
        self.philosophies_path = os.path.abspath(philosophies_path)
        self.philosophies: Dict[str, Any] = {}
        self._load_philosophies()

    def _load_philosophies(self):
        if not os.path.exists(self.philosophies_path):
            raise FileNotFoundError(f"Config filosofie non trovato: {self.philosophies_path}")
        with open(self.philosophies_path, "r", encoding="utf-8") as f:
            index = json.load(f)
        base_dir = os.path.dirname(self.philosophies_path)
        ph = index.get("philosophies", {})
        for key, rel_path in ph.items():
            full = os.path.join(base_dir, rel_path)
            if not os.path.exists(full):
                print(f"[WARN] Filosofia mancante: {full}")
                continue
            with open(full, "r", encoding="utf-8") as fph:
                self.philosophies[key] = json.load(fph)

    def _pass_screens(self, stock: Dict[str, Any], screens: List[Dict[str, Any]]) -> Tuple[bool, str]:
        for s in screens:
            field, op, val = s.get("field"), s.get("op"), s.get("value")
            a = stock.get(field)
            fn = OPERATORS.get(op)
            if fn is None:
                return False, f"Operatore non supportato: {op}"
            if not fn(a, val):
                return False, f"Filtro fallito: {field} {op} {val} (val={a})"
        return True, ""

    def _score_stock(self, stock: Dict[str, Any], rules: Dict[str, Any]) -> Tuple[int, List[str]]:
        w = rules.get("weights", {})
        rationales = []
        score = 0.0
        if "valuation" in w:
            sc = _scale_inv(stock.get("ev_ebit"), tgt=14, maxv=30)
            score += w["valuation"] * sc
            rationales.append(f"Valuation score={round(sc,2)}")
        if "quality" in w:
            sc = _scale(stock.get("roic"), tgt=0.15, maxv=0.30)
            score += w["quality"] * sc
            rationales.append(f"Quality score={round(sc,2)}")
        if "moat" in w:
            sc = _scale(stock.get("moat_score"), tgt=0.7, maxv=1.0)
            score += w["moat"] * sc
            rationales.append(f"Moat score={round(sc,2)}")
        if "growth" in w:
            sc = _scale(stock.get("revenue_cagr_5y"), tgt=0.2, maxv=0.5)
            score += w["growth"] * sc
            rationales.append(f"Growth score={round(sc,2)}")
        custom = rules.get("custom_rules", [])
        for cr in custom:
            field, op, val, wt = cr["field"], cr["op"], cr["value"], cr.get("weight", 0.0)
            passed = OPERATORS.get(op, lambda a,b: False)(stock.get(field), val)
            if passed:
                score += wt
                rationales.append(f"+{wt} su {field} {op} {val}")
        return int(round(score * 100)), rationales

    def _macro_overlay(self, rec: Dict[str, Any], macro: Dict[str, Any], rules: Dict[str, Any]) -> None:
        overlay = rules.get("macro_overlay")
        if not overlay or not macro: 
            return
        regime = f"{macro.get('inflation_trend','?')}_{macro.get('growth_trend','?')}"
        tilts = overlay.get("tilts", {}).get(regime)
        if not tilts: 
            return
        alloc = rec.setdefault("allocation", {})
        for asset, delta in tilts.items():
            alloc[asset] = round(alloc.get(asset, 0) + delta, 4)
        rec.setdefault("rationale", []).append(f"Macro overlay {regime}: {tilts}")

    def generate_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        stocks = data.get("stocks_data", [])
        macro = data.get("macro_data", {})
        out: Dict[str, Any] = {"by_philosophy": {}}

        for name, rules in self.philosophies.items():
            ph_rec = {"watchlist": [], "rationale": [], "risk_flags": [], "allocation": {}}
            screens = rules.get("screens", [])

            for st in stocks:
                ok, why = self._pass_screens(st, screens)
                if not ok:
                    continue
                sc, ras = self._score_stock(st, rules)
                if sc >= rules.get("min_score", 70):
                    ph_rec["watchlist"].append({"symbol": st["symbol"], "score": sc})
                    ph_rec["rationale"].append(f"{st['symbol']}: " + "; ".join(ras))

            base_alloc = rules.get("base_allocation", {})
            ph_rec["allocation"] = base_alloc.copy()
            self._macro_overlay(ph_rec, macro, rules)

            if ph_rec["allocation"]:
                s = sum(ph_rec["allocation"].values())
                if s > 0:
                    for k in list(ph_rec["allocation"].keys()):
                        ph_rec["allocation"][k] = round(ph_rec["allocation"][k] / s, 4)

            out["by_philosophy"][name] = ph_rec

        out["summary"] = {
            "total_watchlist": sorted({w["symbol"] for ph in out["by_philosophy"].values() for w in ph.get("watchlist", [])}),
            "notes": "Allocations normalizzate per filosofia; applicati overlay macro se presenti."
        }
        return out