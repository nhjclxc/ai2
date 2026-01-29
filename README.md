# ai2

深度学习仓库2

[前置](https://github.com/nhjclxc/ai)

基础环境搭建

```shell
conda create -n ai2 python=3.10
conda activate ai2
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels conda-forge
conda config --set channel_priority strict

# 安装机器学习常用包
conda install numpy pandas matplotlib scikit-learn
conda install -c conda-forge jupyterlab
# 安装pytorch深度学习常用包
conda install pytorch torchvision torchaudio cpuonly -c pytorch
# 生成包依赖
pip freeze > requirements.txt
```

# 学习资料

## 01_py

1. [官方语法文档](https://docs.python.org/zh-cn/3.10/)
1. [官方API文档](https://docs.python.org/zh-cn/3.10/library/index.html)
2. [【全748集】目前B站最全最细的Python零基础全套教程，2024最新版，包含所有干货！七天就能从小白到大神！少走99%的弯路！存下吧！很难找全的！](https://www.bilibili.com/video/BV1rpWjevEip)

## 02_ml

### 文档

1. [Numpy](https://numpy.org/doc/stable/)、[Numpy中文](https://numpy.com.cn/doc/stable/index.html)

### 视频

1. [尚硅谷机器学习](https://www.bilibili.com/video/BV1BYe4z5E9z)
3. [【莫烦Python】Numpy & Pandas (数据处理教程)](https://www.bilibili.com/video/BV1Ex411L7oT)
4. [numpy+pandas+matplotlib数据分析](https://www.bilibili.com/video/BV1D9GLzyEL6)
5. [scipy](https://www.bilibili.com/video/BV1gB4y197dm/)、[sympy]()
6. [sklearn](https://www.bilibili.com/video/BV1vJ41187hk)、[sklearn上](https://www.bilibili.com/video/BV1Ch411x7xB/)、[sklearn中](https://www.bilibili.com/video/BV1WL4y1H7rD/)、[sklearn下](https://www.bilibili.com/video/BV1Ng411K7H6)

## 03_dl

1. [尚硅谷深度学习](https://www.bilibili.com/video/BV1MRJmzSEaa)
2.

# 可视化网址

# 相关学习网址

1.

# 数据集

1. [kaggle](https://www.kaggle.com/datasets)

