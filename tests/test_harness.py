"""Tests for task analyzer metrics and input validation."""

from datetime import datetime

import pytest

from src.task_analyzer import InvalidTaskDataException, TaskAnalyzer


def test_analyze_success_calculates_metrics_and_priority_counts() -> None:
    """Calculate exact metrics for completed and pending tasks."""
    tasks = [
        {
            "id": 1,
            "titulo": "Tarefa concluída no prazo",
            "prioridade": "ALTA",
            "data_criacao": datetime(2026, 1, 1, 9),
            "data_conclusao": datetime(2026, 1, 2, 9),
            "prazo_limite": datetime(2026, 1, 2, 9),
            "status": "CONCLUIDA",
        },
        {
            "id": 2,
            "titulo": "Tarefa concluída com atraso",
            "prioridade": "MEDIA",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-03T09:00:00",
            "prazo_limite": "2026-01-02T09:00:00",
            "status": "CONCLUIDA",
        },
        {
            "id": 3,
            "titulo": "Tarefa pendente",
            "prioridade": "BAIXA",
            "data_criacao": "2026-01-01",
            "data_conclusao": None,
            "prazo_limite": "2026-01-05",
            "status": "PENDENTE",
        },
    ]

    result = TaskAnalyzer(tasks).analyze()

    assert result == {
        "total_tarefas": 3,
        "total_concluidas": 2,
        "tempo_medio_horas": 36.0,
        "taxa_atraso_percentual": 50.0,
        "por_prioridade": {
            "BAIXA": {"total": 1, "concluidas": 0, "pendentes": 1},
            "MEDIA": {"total": 1, "concluidas": 1, "pendentes": 0},
            "ALTA": {"total": 1, "concluidas": 1, "pendentes": 0},
        },
    }


def test_analyze_rejects_completion_before_creation() -> None:
    """Raise the domain exception for inconsistent task chronology."""
    task = {
        "id": 1,
        "titulo": "Cronologia inválida",
        "prioridade": "ALTA",
        "data_criacao": "2026-01-02",
        "data_conclusao": "2026-01-01",
        "prazo_limite": "2026-01-05",
        "status": "CONCLUIDA",
    }

    with pytest.raises(
        InvalidTaskDataException, match="data_conclusao anterior"
    ):
        TaskAnalyzer([task]).analyze()


def test_analyze_empty_task_list_returns_zero_metrics() -> None:
    """Return zero-valued metrics for an empty list."""
    result = TaskAnalyzer([]).analyze()

    assert result["total_tarefas"] == 0
    assert result["total_concluidas"] == 0
    assert result["tempo_medio_horas"] == 0.0
    assert result["taxa_atraso_percentual"] == 0.0


def test_analyze_without_completed_tasks_avoids_division_by_zero() -> None:
    """Return zero averages and late rate when all tasks are pending."""
    task = {
        "id": 1,
        "titulo": "Tarefa pendente",
        "prioridade": "BAIXA",
        "data_criacao": "2026-01-01",
        "data_conclusao": None,
        "prazo_limite": "2026-01-05",
        "status": "PENDENTE",
    }

    result = TaskAnalyzer([task]).analyze()

    assert result["tempo_medio_horas"] == 0.0
    assert result["taxa_atraso_percentual"] == 0.0
