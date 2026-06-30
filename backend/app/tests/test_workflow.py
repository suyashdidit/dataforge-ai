from pathlib import Path


def test_github_workflow_exists_and_is_configured() -> None:
    workflow_path = Path(__file__).resolve().parents[3] / ".github" / "workflows" / "dataforge.yml"
    assert workflow_path.exists(), f"Workflow file not found: {workflow_path}"

    content = workflow_path.read_text()
    assert "on:" in content
    assert "pull_request:" in content
    assert "permissions:" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content
    assert "python ./dataforge analyze-change . --markdown" in content
    assert "actions/github-script@v7" in content
