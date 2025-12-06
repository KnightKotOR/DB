import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import dbs_router, stats_router, md_router, query_router, alias_router

app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dbs_router.router)
app.include_router(stats_router.router)
app.include_router(md_router.router)
app.include_router(query_router.router)
app.include_router(alias_router.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)