"""从构建目录提供静态资源，浏览器直接打开前端路由时返回入口页。"""

import re
from pathlib import Path

from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.types import Scope


# Vite 构建的资源名以连字符、八位内容哈希和扩展名结尾。
HASHED_ASSET = re.compile(r"assets/(?:[^/]+/)*[^/]+-[A-Za-z0-9_-]{8}\.[^/.]+")


class Frontend(StaticFiles):
    def __init__(self, directory: Path):
        if not (directory / "index.html").is_file():
            raise RuntimeError("缺少前端入口，请先运行 deploy/run.sh --build")
        super().__init__(directory=directory)

    async def get_response(self, path: str, scope: Scope) -> Response:
        # Starlette 在 Windows 上传进来的是系统路径（assets\absent），先统一成 / 再判断
        route = path.replace("\\", "/")
        if route == "api" or route.startswith("api/"):
            raise HTTPException(404)
        try:
            response = await super().get_response(path, scope)
        except HTTPException as exc:
            if exc.status_code != 404 or route.startswith("assets/") or Path(route).suffix:
                raise
            response = await super().get_response("index.html", scope)
        response.headers["Cache-Control"] = (
            "public, max-age=31536000, immutable" if HASHED_ASSET.fullmatch(route) else "no-cache"
        )
        return response
