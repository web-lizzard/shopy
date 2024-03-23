class CartNotReadyError(Exception):
    def __init__(self, message: str | None) -> None:
        super().__init__(f"Cart is not ready to execute: {message}")
