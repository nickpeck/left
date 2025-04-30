from dataclasses import dataclass


@dataclass
class TestResult:
    test_name: str
    passed: bool
    stacktrace: str
    duration: float = 0.0
