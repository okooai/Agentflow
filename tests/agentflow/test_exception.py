# imports - module imports
from agentflow.exception import AgentflowError

# imports - test imports
import pytest


def test_agentflow_error():
    with pytest.raises(AgentflowError):
        raise AgentflowError
