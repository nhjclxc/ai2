

非常好的问题 👍，这是机器学习入门到进阶都必须非常清楚的一个核心知识点。
模型评估方法本质上是：**衡量模型在训练集和测试集上表现的好坏**。
根据任务类型（分类 / 回归 / 聚类等）不同，评估方法也不同。

下面我系统、清晰地为你整理一份：

---

## 🧭 一、整体框架总览

| 任务类型       | 常用评估指标                  | 典型函数（sklearn中）                                                                                       |
| ---------- | ----------------------- | ---------------------------------------------------------------------------------------------------- |
| **分类任务**   | 准确率、精确率、召回率、F1、AUC、混淆矩阵 | `accuracy_score`, `precision_score`, `recall_score`, `f1_score`, `roc_auc_score`, `confusion_matrix` |
| **回归任务**   | MSE、RMSE、MAE、R²         | `mean_squared_error`, `mean_absolute_error`, `r2_score`                                              |
| **聚类任务**   | 轮廓系数、纯度、NMI、ARI         | `silhouette_score`, `normalized_mutual_info_score`, `adjusted_rand_score`                            |
| **模型泛化评估** | 交叉验证、留出法、Bootstrap      | `cross_val_score`, `train_test_split`                                                                |

---

## 🧩 二、分类模型评估方法

### 1️⃣ 准确率（Accuracy）

[
Accuracy = \frac{正确预测的样本数}{总样本数}
]

简单但容易受类别不平衡影响。
比如在癌症预测中 99% 是健康，模型全预测“健康”也能有 99% 准确率。

---

### 2️⃣ 精确率（Precision）与召回率（Recall）

| 概念            | 含义                  | 公式             |
| ------------- | ------------------- | -------------- |
| 精确率 Precision | 被预测为正的样本中，实际为正的比例   | TP / (TP + FP) |
| 召回率 Recall    | 实际为正的样本中，被正确预测为正的比例 | TP / (TP + FN) |

例子：

* 精确率高：误报少
* 召回率高：漏报少
* 想平衡两者，就看 F1 分数。

---

### 3️⃣ F1 值（综合平衡指标）

[
F1 = 2 \times \frac{Precision \times Recall}{Precision + Recall}
]

特别适合类别不平衡问题。

---

### 4️⃣ ROC 曲线与 AUC 值

* ROC 曲线：横轴是 FPR（假正率），纵轴是 TPR（召回率）
* AUC：ROC 曲线下面积，越接近 1 说明模型区分能力越强。

---

### 5️⃣ 混淆矩阵（Confusion Matrix）

矩阵形式总结分类情况：

| 实际\预测    | Positive | Negative |
| -------- | -------- | -------- |
| Positive | TP       | FN       |
| Negative | FP       | TN       |

能一眼看出分类模型的优缺点。

---

## 🧮 三、回归模型评估方法

| 指标                           | 含义            | 公式 / 说明                                |                 |   |
| ---------------------------- | ------------- | -------------------------------------- | --------------- | - |
| **MSE** (Mean Squared Error) | 均方误差          | (\frac{1}{n}\sum (y_i - \hat{y_i})^2)  |                 |   |
| **RMSE**                     | 均方根误差（与原单位一致） | (\sqrt{MSE})                           |                 |   |
| **MAE**                      | 平均绝对误差        | (\frac{1}{n}\sum                       | y_i - \hat{y_i} | ) |
| **R²** (决定系数)                | 模型解释能力        | (1 - \frac{SS_{res}}{SS_{tot}})，越接近1越好 |                 |   |

---

## 🧠 四、模型泛化能力评估（验证方法）

### 1️⃣ 留出法（Hold-out）

将数据随机分为：

* 训练集（train）
* 验证集（validation）
* 测试集（test）

例：7:2:1 比例。

---

### 2️⃣ 交叉验证（Cross Validation）

最常见是 **K 折交叉验证 (K-Fold)**：

* 将数据分成 K 份；
* 每次用 K−1 份训练，1 份验证；
* 平均 K 次结果作为评估分数。

👉 更稳健，减少随机性。

---

### 3️⃣ Bootstrap（自助采样法）

* 有放回地随机抽样形成训练集；
* 未抽到的样本作为验证集；
* 常用于小样本模型评估。

---

## 🧮 五、聚类模型评估方法（无监督）

| 指标                                      | 含义                      |
| --------------------------------------- | ----------------------- |
| **轮廓系数 (Silhouette Score)**             | 衡量类内紧密度与类间分离度，范围 [-1,1] |
| **NMI (Normalized Mutual Information)** | 与真实标签一致性（如果有标签）         |
| **ARI (Adjusted Rand Index)**           | 衡量聚类分配与真实分类的一致性         |

---

## 📘 六、总结表（一句话记忆版）

| 任务   | 核心评估指标             | 说明           |
| ---- | ------------------ | ------------ |
| 分类   | 准确率、精确率、召回率、F1、AUC | 衡量分类正确与否、平衡性 |
| 回归   | MSE、MAE、R²         | 衡量预测值和真实值差距  |
| 聚类   | 轮廓系数、NMI           | 衡量聚类结果好坏     |
| 模型验证 | 交叉验证、留出法           | 衡量模型泛化能力     |

---

## 💡 七、代码示例（以分类为例）

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

y_true = [0, 1, 1, 0, 1, 0]
y_pred = [0, 1, 0, 0, 1, 1]

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Precision:", precision_score(y_true, y_pred))
print("Recall:", recall_score(y_true, y_pred))
print("F1:", f1_score(y_true, y_pred))
print("AUC:", roc_auc_score(y_true, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_true, y_pred))
```

---

是否希望我帮你画一张「机器学习模型评估方法思维导图」？
比如从“分类 / 回归 / 聚类 / 泛化评估”四个方向发散，能更直观地掌握全局结构。
