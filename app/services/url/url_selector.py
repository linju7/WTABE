from app.services.security import url

def url_selector(server, instance):
    target_url = url[server][instance]["service"]
    
    if target_url:
        return target_url
    else:
        raise ValueError(f"Invalid server or instance: {server}, {instance}")