import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "lambda_saleor_app.app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
