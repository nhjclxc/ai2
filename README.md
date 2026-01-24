# ai2
深度学习仓库2

[前置](https://github.com/nhjclxc/ai)

基础环境搭建
```shell
conda create -n ai2 python=3.10
conda activate ai2
# 安装机器学习常用包
conda install numpy pandas matplotlib scikit-learn jupyter
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
1. [尚硅谷机器学习](https://www.bilibili.com/video/BV1BYe4z5E9z)
2. [尚硅谷深度学习](https://www.bilibili.com/video/BV1MRJmzSEaa)

# 可视化网址

# 相关学习网址
1. 


# 数据集
1. [kaggle](https://www.kaggle.com/datasets)



(ai2) C:\Users\nhjcl>conda list
# packages in environment at D:\develop\miniconda3\envs\ai2:
#
# Name                     Version          Build                  Channel
blas                       1.0              mkl                    https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
bzip2                      1.0.8            h2bbff1b_6             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
ca-certificates            2025.12.2        haa95532_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
expat                      2.7.3            h885b0b7_4             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
filelock                   3.20.2           pypi_0                 pypi
fsspec                     2025.12.0        pypi_0                 pypi
intel-openmp               2025.0.0         haa95532_1164          https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
jinja2                     3.1.6            pypi_0                 pypi
libexpat                   2.7.3            h885b0b7_4             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
libffi                     3.4.4            hd77b12b_1             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
libhwloc                   2.12.1           default_hfa10c62_1000  https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
libiconv                   1.16             h2bbff1b_3             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
libxml2                    2.13.9           h6201b9f_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
libzlib                    1.3.1            h02ab6af_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
markupsafe                 3.0.3            pypi_0                 pypi
mkl                        2025.0.0         h5da7b33_930           https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
mkl-service                2.5.2            py310h0b37514_0        https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
mkl_fft                    2.1.1            py310h300f80d_0        https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
mkl_random                 1.3.0            py310ha5e6156_0        https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
mpmath                     1.3.0            pypi_0                 pypi
networkx                   3.4.2            pypi_0                 pypi
numpy                      2.2.5            py310h7894be3_2        https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
numpy-base                 2.2.5            py310h7794460_2        https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
openssl                    3.0.18           h543e019_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
pip                        25.3             pyhc872135_0           https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
python                     3.10.19          h981015d_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
setuptools                 80.9.0           py310haa95532_0        https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
sqlite                     3.51.0           hda9a48d_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
sympy                      1.14.0           pypi_0                 pypi
tbb                        2022.3.0         h90c84d6_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
tbb-devel                  2022.3.0         h90c84d6_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
tk                         8.6.15           hf199647_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
torch                      2.9.1            pypi_0                 pypi
typing-extensions          4.15.0           pypi_0                 pypi
tzdata                     2025b            h04d1e81_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
ucrt                       10.0.22621.0     haa95532_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
vc                         14.3             h2df5915_10            https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
vc14_runtime               14.44.35208      h4927774_10            https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
vs2015_runtime             14.44.35208      ha6b5a95_10            https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
wheel                      0.45.1           py310haa95532_0        https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
xz                         5.6.4            h4754444_1             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
zlib                       1.3.1            h02ab6af_0             https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main