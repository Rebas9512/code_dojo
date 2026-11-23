"""从构建目录提供静态资源，浏览器直接打开前端路由时返回入口页。"""

from pathlib import Path

from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.types import Scope


class Frontend(StaticFiles):
    def __init__(self, directory: Path):
        if not (directory / "index.html").is_file():
            raise RuntimeError("缺少前端入口，请先运行 deploy/run.sh --build")
        super().__init__(directory=directory)

    async def get_response(self, path: str, scope: Scope) -> Response:
        if path == "api" or path.startswith("api/"):
            raise HTTPException(404)
        try:
            return await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404 or path.startswith("assets/") or Path(path).suffix:
                raise
        return await super().get_response("index.html", scope)
