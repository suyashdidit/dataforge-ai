from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.scanner.models import FileType
from app.scanner.service import ScannerService

client = TestClient(app)


def test_scanner_detects_sql_files(tmp_path: Path) -> None:
    sql_file = tmp_path / "query.sql"
    sql_file.write_text("SELECT 1;")

    service = ScannerService()
    metadata = service.scan(str(tmp_path))

    assert metadata.scanned_files == 1
    assert len(metadata.sql_files) == 1
    assert metadata.sql_files[0].path.endswith("query.sql")
    assert metadata.sql_files[0].type == FileType.SQL


def test_scanner_returns_metadata(tmp_path: Path) -> None:
    (tmp_path / "models").mkdir()
    model_file = tmp_path / "models" / "model.sql"
    model_file.write_text("SELECT 2;")

    service = ScannerService()
    metadata = service.scan(str(tmp_path))

    assert metadata.project_name == tmp_path.name
    assert metadata.scanned_files == 1
    assert metadata.dbt_models[0].type == FileType.DBT_MODEL


def test_scan_api_endpoint(tmp_path: Path) -> None:
    (tmp_path / "query.sql").write_text("SELECT 3;")

    response = client.post("/scan/", json={"path": str(tmp_path)})

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["dbt_detected"] is False
    assert json_data["scanned_files"] == 1
    assert json_data["sql_files"][0]["type"] == "sql"
    assert json_data["detected_dependencies"] == []
    assert json_data["risks"] == []
