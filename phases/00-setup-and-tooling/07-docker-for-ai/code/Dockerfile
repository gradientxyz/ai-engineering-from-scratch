FROM nvidia/cuda:12.8.0-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
# 设置 pip 国内镜像源（全局生效）
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 安装 Python 3.12 及其依赖
# 注意：已移除 python3.12-distutils，因为它在 Ubuntu 24.04 / Python 3.12 中不再存在
# 更换 apt 源为清华镜像（加速下载）
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-venv \
        python3.12-dev \
        python3-pip \
        git \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# 设置 python 别名
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# 安装 PyTorch (针对 CUDA 12.8)
RUN python -m pip install --no-cache-dir --break-system-packages \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu128

# 安装其他数据科学库（会自动使用 PIP_INDEX_URL 的镜像）
RUN python -m pip install --no-cache-dir --break-system-packages \
    numpy \
    pandas \
    scikit-learn \
    matplotlib \
    jupyter \
    transformers \
    datasets \
    accelerate \
    safetensors

WORKDIR /workspace

VOLUME ["/workspace", "/models"]

EXPOSE 8888

CMD ["python"]
