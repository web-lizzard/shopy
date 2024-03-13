

if __name__ == "__main__":
    import uvicorn
    from server.main import create_app

    uvicorn.run(f'{__name__}:{create_app.__name__}', port=80, host='0.0.0.0', factory=True, server_header=True)