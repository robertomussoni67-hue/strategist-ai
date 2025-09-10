class UserProfile:
    def __init__(self, name="Roberto", age=45, risk_level="moderate", horizon_years=10, goal="wealth_growth", style="balanced"):
        self.name = name
        self.age = age
        self.risk_level = risk_level  # "conservative", "moderate", "aggressive"
        self.horizon_years = horizon_years
        self.goal = goal  # "wealth_growth", "income", "capital_preservation"
        self.style = style  # "balanced", "equity_focus", "bond_focus"

    def get_preferences(self):
        # Mappa profilo → preferenze allocative
        if self.risk_level == "conservative":
            return {
                "equity_max": 0.40,
                "bond_min": 0.50,
                "gold_max": 0.10,
                "cash_min": 0.10
            }
        elif self.risk_level == "aggressive":
            return {
                "equity_min": 0.60,
                "bond_max": 0.30,
                "commodities_max": 0.20,
                "cash_max": 0.05
            }
        else:  # moderate
            return {
                "equity_min": 0.40,
                "bond_min": 0.40,
                "gold_max": 0.15,
                "cash_max": 0.10
            }

    def describe(self):
        return f"{self.name}, {self.age} anni, profilo {self.risk_level}, orizzonte {self.horizon_years} anni, obiettivo: {self.goal}, stile: {self.style}"