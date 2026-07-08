from pathlib import Path


def test_required_files_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "tech_agent" / "agent.py").exists()
    assert (root / "mcp_servers" / "trends_server.py").exists()
    assert (root / "Dockerfile").exists()
    assert (root / "infra" / "terraform" / "main.tf").exists()


def test_mcp_servers_exist():
    root = Path(__file__).resolve().parents[1]
    expected = [
        "search_server.py",
        "docs_server.py",
        "github_server.py",
        "trends_server.py",
        "code_examples_server.py",
        "kubernetes_server.py",
        "terraform_server.py",
        "aws_server.py",
        "gcp_server.py",
        "devops_server.py",
    ]
    for name in expected:
        assert (root / "mcp_servers" / name).exists()
