# src/modules/philosophy_config.py

PHILOSOPHIES = {
    "all_seasons": {
        "label": "All Seasons (Ray Dalio)",
        "base": {
            "equity": 0.30,
            "gov_bonds_long": 0.40,
            "gov_bonds_mid": 0.15,
            "gold": 0.075,
            "commodities": 0.075,
            "cash": 0.00
        },
        "tilts": {
            "growth_up_infl_down": {"equity": +0.10, "gov_bonds_long": -0.10, "commodities": -0.03},
            "growth_down_infl_down": {"gov_bonds_long": +0.10, "equity": -0.10, "gold": +0.02},
            "growth_up_infl_up": {"commodities": +0.08, "gold": +0.02, "gov_bonds_long": -0.10},
            "growth_down_infl_up": {"gold": +0.08, "commodities": +0.05, "equity": -0.10}
        },
        "constraints": {
            "equity_min": 0.20, "equity_max": 0.50,
            "commodities_max": 0.20, "gold_max": 0.15,
            "bond_total_min": 0.30
        }
    },
    "bogle_core": {
        "label": "Bogle Core (Indexing)",
        "base": {"equity": 0.60, "bond_agg": 0.35, "cash": 0.05},
        "tilts": {},
        "constraints": {"equity_min": 0.40, "equity_max": 0.80}
    }
}