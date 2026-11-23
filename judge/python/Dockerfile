# code-dojo Python 判题镜像：原生 CPython 3.14 + 判题程序。
# 构建：docker build -t code-dojo-judge-py:3.14 judge/python
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=0

COPY harness.py dojo_constraints.py /judge/
RUN chmod 0755 /judge && chmod 0444 /judge/*.py

USER 65534:65534
WORKDIR /work
ENTRYPOINT ["python", "-I", "/judge/harness.py"]
