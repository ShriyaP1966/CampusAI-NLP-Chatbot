from __future__ import annotations

import pytest

from campusai import CampusAI


@pytest.fixture(scope="session")
def bot() -> CampusAI:
    return CampusAI.from_directory()
