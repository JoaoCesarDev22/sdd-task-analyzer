"""Analyze task completion time, delays, and priority distribution."""

from datetime import date, datetime
from typing import Final, TypedDict


PRIORITIES: Final[tuple[str, ...]] = ("BAIXA", "MEDIA", "ALTA")
STATUSES: Final[tuple[str, ...]] = ("CONCLUIDA", "PENDENTE")
TASK_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "id",
        "titulo",
        "prioridade",
        "data_criacao",
        "data_conclusao",
        "prazo_limite",
        "status",
    }
)


class InvalidTaskDataException(ValueError):
    """Raised when task data is invalid or temporally inconsistent."""


class PriorityMetrics(TypedDict):
    """Task counts for a single priority."""

    total: int
    concluidas: int
    pendentes: int


class AnalysisResult(TypedDict):
    """Metrics returned by :meth:`TaskAnalyzer.analyze`."""

    total_tarefas: int
    total_concluidas: int
    tempo_medio_horas: float
    taxa_atraso_percentual: float
    por_prioridade: dict[str, PriorityMetrics]


class TaskAnalyzer:
    """Calculate aggregate metrics for a collection of tasks.

    Each task must contain ``id``, ``titulo``, ``prioridade``,
    ``data_criacao``, ``data_conclusao``, ``prazo_limite``, and ``status``.
    Dates may be ``datetime`` objects, ``date`` objects, or ISO-8601 strings.
    A pending task may have ``None`` for its completion date.
    """

    def __init__(self, tasks: list[dict[str, object]]) -> None:
        """Initialize the analyzer with task dictionaries.

        Args:
            tasks: Tasks to validate and analyze.
        """
        self._tasks = tasks

    def analyze(self) -> AnalysisResult:
        """Validate tasks and calculate aggregate metrics.

        The late rate is the percentage of completed tasks completed after
        their deadline. The average duration includes completed tasks only;
        both metrics are ``0.0`` when there are no completed tasks.

        Returns:
            A dictionary containing totals, time and delay metrics, and
            per-priority task counts.

        Raises:
            InvalidTaskDataException: If a task is malformed or has
                inconsistent dates.
        """
        priority_metrics: dict[str, PriorityMetrics] = {
            priority: {"total": 0, "concluidas": 0, "pendentes": 0}
            for priority in PRIORITIES
        }
        completed_count = 0
        late_count = 0
        total_duration_seconds = 0.0

        for index, task in enumerate(self._tasks):
            missing_fields = TASK_FIELDS.difference(task)
            if missing_fields:
                raise InvalidTaskDataException(
                    f"Tarefa no índice {index}: campos ausentes "
                    f"{', '.join(sorted(missing_fields))}."
                )

            task_id = task["id"]
            if task_id is None or not isinstance(task.get("titulo"), str):
                raise InvalidTaskDataException(
                    f"Tarefa {task_id!r}: id e titulo devem ser informados."
                )
            priority = task.get("prioridade")
            status = task.get("status")
            if not isinstance(priority, str) or priority not in PRIORITIES:
                raise InvalidTaskDataException(
                    f"Tarefa {task_id!r}: prioridade inválida."
                )
            if not isinstance(status, str) or status not in STATUSES:
                raise InvalidTaskDataException(
                    f"Tarefa {task_id!r}: status inválido."
                )

            created_at = self._parse_date(
                task.get("data_criacao"), task_id, "data_criacao"
            )
            deadline = self._parse_date(
                task.get("prazo_limite"), task_id, "prazo_limite"
            )
            completed_value = task.get("data_conclusao")
            completed_at: datetime | None = None
            if completed_value is not None:
                completed_at = self._parse_date(
                    completed_value, task_id, "data_conclusao"
                )
                self._ensure_comparable(created_at, completed_at, task_id)
                if completed_at < created_at:
                    raise InvalidTaskDataException(
                        f"Tarefa {task_id!r}: data_conclusao anterior "
                        "a data_criacao."
                    )

            self._ensure_comparable(created_at, deadline, task_id)
            if deadline < created_at:
                raise InvalidTaskDataException(
                    f"Tarefa {task_id!r}: prazo_limite anterior "
                    "a data_criacao."
                )
            if status == "CONCLUIDA" and completed_at is None:
                raise InvalidTaskDataException(
                    f"Tarefa {task_id!r}: tarefa concluída sem data_conclusao."
                )

            metrics = priority_metrics[priority]
            metrics["total"] += 1
            if status == "CONCLUIDA":
                self._ensure_comparable(deadline, completed_at, task_id)
                completed_count += 1
                metrics["concluidas"] += 1
                total_duration_seconds += (
                    completed_at - created_at
                ).total_seconds()
                if completed_at > deadline:
                    late_count += 1
            else:
                metrics["pendentes"] += 1

        average_hours = (
            total_duration_seconds / 3600 / completed_count
            if completed_count
            else 0.0
        )
        late_rate = (
            late_count / completed_count * 100 if completed_count else 0.0
        )
        return {
            "total_tarefas": len(self._tasks),
            "total_concluidas": completed_count,
            "tempo_medio_horas": average_hours,
            "taxa_atraso_percentual": late_rate,
            "por_prioridade": priority_metrics,
        }

    @staticmethod
    def _parse_date(value: object, task_id: object, field: str) -> datetime:
        """Convert an accepted date value to a datetime.

        Args:
            value: A date, datetime, or ISO-8601 string.
            task_id: Identifier used in validation messages.
            field: Name of the field being parsed.

        Returns:
            The parsed datetime.

        Raises:
            InvalidTaskDataException: If the value is not a supported date.
        """
        try:
            if isinstance(value, datetime):
                return value
            if isinstance(value, date):
                return datetime.combine(value, datetime.min.time())
            if isinstance(value, str):
                return datetime.fromisoformat(value)
        except ValueError as error:
            raise InvalidTaskDataException(
                f"Tarefa {task_id!r}: {field} inválida."
            ) from error
        raise InvalidTaskDataException(
            f"Tarefa {task_id!r}: {field} deve ser uma data, datetime ou "
            "string ISO-8601."
        )

    @staticmethod
    def _ensure_comparable(
        first: datetime, second: datetime | None, task_id: object
    ) -> None:
        """Reject dates with incompatible timezone awareness.

        Args:
            first: First datetime to compare.
            second: Second datetime to compare, if present.
            task_id: Identifier used in validation messages.

        Raises:
            InvalidTaskDataException: If only one datetime is timezone-aware.
        """
        if second is None:
            return
        if (first.utcoffset() is None) != (second.utcoffset() is None):
            raise InvalidTaskDataException(
                f"Tarefa {task_id!r}: datas com fusos horários incompatíveis."
            )
