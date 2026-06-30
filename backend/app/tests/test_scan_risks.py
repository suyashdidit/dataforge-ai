from pathlib import Path

from app.scanner.models import FileType
from app.scanner.service import ScannerService


def test_scanner_detects_risks_and_dependencies(tmp_path: Path) -> None:
    sql_text = "SELECT * FROM {{ ref('my_model') }} JOIN {{ source('raw', 'users') }} ON 1=1;"
    file_path = tmp_path / "models" / "risk_model.sql"
    file_path.parent.mkdir(parents=True)
    file_path.write_text(sql_text)

    service = ScannerService()
    metadata = service.scan(str(tmp_path))

    assert metadata.scanned_files == 1
    assert metadata.dbt_models[0].type == FileType.DBT_MODEL
    assert "my_model" in metadata.detected_dependencies
    assert "raw.users" in metadata.detected_dependencies
    assert "select_star_usage" in metadata.risks
