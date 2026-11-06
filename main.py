"""CSV-reader implementation for the fiscal year 2569 visitor report."""

import csv
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException

DATA_FILE = Path(__file__).parent / "zoo_visitors_january_2569.csv"
app = FastAPI(title="Zoo Visitors Report API", version="1.0.0")


def convert(value: str) -> Any:
    cleaned = value.strip()
    if cleaned == "":
        return None
    try:
        return int(cleaned.replace(",", ""))
    except ValueError:
        return cleaned


def csv_to_json_rows() -> list[dict[str, Any]]:
    if not DATA_FILE.is_file():
        raise HTTPException(status_code=500, detail="Required CSV file is not in the project folder")

    try:
        with DATA_FILE.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            columns = next(reader, [])
            names = [col.strip() for col in columns]
            items: list[dict[str, Any]] = []
            for cells in reader:
                item = {
                    name: convert(cells[index]) if index < len(cells) else None
                    for index, name in enumerate(names)
                    if name
                }
                if any(value is not None for value in item.values()):
                    items.append(item)
            return items
    except (OSError, UnicodeError, csv.Error, StopIteration) as exc:
        raise HTTPException(status_code=500, detail=f"CSV processing error: {exc}") from exc


@app.get("/api/zoo-visitors", tags=["Data.go.th"])
def list_visitors() -> dict[str, Any]:
    data = csv_to_json_rows()
    return {
        "source": "Data.go.th - Open Government Data of Thailand",
        "dataset": "ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569",
        "dataset_url": "https://data.go.th/dataset/zoo-visitors2569",
        "resource_id": "0ecc96cf-d914-42a1-b184-dbbd013c3c9c",
        "fiscal_year": 2569,
        "records_count": len(data),
        "records": data,
    }


@app.get("/", include_in_schema=False)
def index() -> dict[str, str]:
    return {"message": "Zoo Visitors Report API", "docs": "/docs"}
