from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time


from app.presentation.routers.user_router import router
from app.presentation.routers.general_routes import router_genereal
from app.presentation.routers.admin_router import router_admin
from app.presentation.routers.todo_router import todo_router
from app.core.logger import logger
from app.core.limiter import Limiter
# ===============

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded , _rate_limit_exceeded_handler)



app.add_middleware(
    CORSMiddleware,
    # It is safe for developing phase but in production it is dangerous
    allow_origins = ['http://localhost:3000'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)
app.include_router(router= router)
app.include_router(router= router_genereal)
app.include_router(router= router_admin)
app.include_router(router= todo_router)



@app.exception_handler(Exception)
async def global_exception_handler(request : Request, exc : Exception):
    if isinstance(exc , HTTPException):
        raise exc
    return JSONResponse(
        status_code= 500,
        content={'detail' : 'Internal server error'}
    )





@app.middleware('http')
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    logger.info(f"{request.method} {request.url.path} ---- {process_time:.4f}s")

    return response
