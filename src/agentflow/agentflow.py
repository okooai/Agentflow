from agentflow.model.hub import Hub

def hub(name):
    hub_ = Hub()
    return hub_.get(name)