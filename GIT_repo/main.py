from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI()

class FinancialInput(BaseModel):
    revenues: Dict[str, float]
    cogs: Dict[str, float]

class YearOutput(BaseModel):
    gross_profit: Optional[float]
    gp_margin: Optional[float]
    cogs_margin: Optional[float]
    yoy_growth: Optional[float]

@app.post("/compute_ratios")
def compute_ratios(data: FinancialInput) -> Dict[str, YearOutput]:
    output = {}
    years = sorted(data.revenues.keys())
    for i, year in enumerate(years):
        rev = data.revenues.get(year)
        cost = data.cogs.get(year)
        if rev is None or cost is None:
            continue
        gp = rev - cost
        gp_margin = gp / rev if rev else None
        cogs_margin = cost / rev if rev else None
        if i > 0:
            prev_year = years[i - 1]
            prev_rev = data.revenues.get(prev_year)
            yoy = (rev - prev_rev) / prev_rev if prev_rev else None
        else:
            yoy = None
        output[year] = YearOutput(
            gross_profit=round(gp, 1),
            gp_margin=round(gp_margin, 4) if gp_margin else None,
            cogs_margin=round(cogs_margin, 4) if cogs_margin else None,
            yoy_growth=round(yoy, 4) if yoy is not None else None,
        )
    return output
