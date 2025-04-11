from app.services.security import url
from app.services.url.url_selector import url_selector

async def move_url(page, server, instance) :
    target_url = url_selector(server, instance)
    await page.goto(target_url)
    return page