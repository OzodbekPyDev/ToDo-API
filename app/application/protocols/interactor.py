from typing import Protocol


class Interactor[Request, Response](Protocol):
    async def __call__(self, request: Request) -> Response:
        raise NotImplementedError
