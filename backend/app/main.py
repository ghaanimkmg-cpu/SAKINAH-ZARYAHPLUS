from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title='NIS Backend',
    version='v1'
)

app.include_router(api_router, prefix='/api/v1')

@app.get('/health', tags=['health'])
async def root_health_check():
    return {
        'status': 'ok',
        'service': 'NIS Backend',
        'version': 'v1'
    }
