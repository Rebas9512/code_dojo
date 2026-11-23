# 先构建 judge/python，再构建此镜像，两者使用同一份判题程序。
FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1

RUN pip install --no-cache-dir numpy==2.5.5 pandas==3.1.1 \
 && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.15.0+cpu

COPY --from=code-dojo-judge-py:3.14 /judge/ /judge/
COPY dojo_*.py /judge/
USER 65534:65534
WORKDIR /work
ENTRYPOINT ["python", "-I", "/judge/harness.py"]
