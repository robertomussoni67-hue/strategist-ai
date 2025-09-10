# src/modules/preferences.py

DEFAULT_PREFERENCES = {
    "philosophy": "all_seasons",
    "region_bias": ["global", "europe"],  # preferenze aree
    "equity_style": ["quality", "growth"],  # stili preferiti
    "exclude_sectors": ["tobacco"],  # esclusioni etiche
    "etf": {"max_ter": 0.30, "domicile_whitelist": ["IE", "LU"], "replication": ["physical"]},
    "etc": {"prefer_physical": True, "issuer_whitelist": [], "gold_only_alloc_cap": 0.15},
    "stocks": {"min_roic": 0, "max_debt_to_equity": 2.0, "min_fcf_yield": 0.0}
}