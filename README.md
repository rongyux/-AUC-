# 点击率模型 AUC 计算方法
<p>对于不平衡数据或倾斜数据，准确率和召回率不能评价分类器好坏了。AUC是一个不错对选择，但是由于点击率预估模型对特殊场景，AUC对计算又不同于二分类问题中对AUC计算。下面总结了广工算法业界通用 对AUC计算方法。

## 一 背景
<dependency>
<p>				正样本（90） 				负样本（10） 		
<p>模型1预测		正（90）					正（10）
<p>模型2预测		正（70）负（20）			正（5）负（5）
<p>结论：
<p>	模型1准确率90%；
<p>	模型2 准确率75%	；
<p>	考虑对正负样本对预测能力，显然模型2要比模型1好，但对于这种正负样本分布不平衡对数据，准确率不能衡量分类器对好坏了，所以需要指标auc解决倾斜样本的<p>评价问题。
<p>二分类混淆矩阵
<p>实际\预测  	0		1
<p>1				TP		FN
<p>0				FP		TN
<p>TPR＝TP/P＝TP／TP＋FN   直观1中猜对多少
<p>FPR＝FP／N＝FP／FP＋TN  直观0中猜错多少
<p>Auc对横纵坐标分别为FPR和TPR，相对于y=x这条直线靠近左上角对分类器性能更好，所以模型2更优。
<p>				TPR				FPR
<p>模型1			90/90＝1			10/10=1
<p>模型2			70/90=0.78			5/10=0.5
 <／dependency>

## 二 研究现状
<dependency>
<p>AUC直观概念，任意取一对正负样本，正样本score大于负样本对概率。 
<p>计算方法：正样本和负样本pair对，auc＝预估正样本score大于负样本score的pair对数／总的pair对数。
<p>E.g. 分别计算模型1和2对auc？
<p>四个样本label为y1=+1, y2=+1, y3=-1, y4=-1
<p>模型1的预测为 y1=0.9, y2=0.5, y3=0.2, y4=0.6
<p>模型2的预测为 y1=0.1, y2=0.9, y3=0.8, y4=0.2
<p>解： 
<p>        模型1： 正样本score大于负样本的pair包括(y1, y3), (y1, y4), (y2, y3)，auc为3/4=0.75
 <p>        模型2： 正样本score大于负样本的pair包括(y2, y3),(y2, y4)，auc为2/4=0.5
 
<p>大量样本对计算，paper《 An introduction to ROC analysis 》（Tom Fawcett）
<p>方法：
 
<p>1按照score对样本排序；
<p>2依次对每个样本，label分对TP增1，否则FP增1。计算每个小梯形的面积。
<p>3累加所有样本，计算auc

<p>代码见：calcu_auc.py
<／dependency>
## 三 点击率模型auc计算方法
<dependency>
<p>考虑点击率模型的场景的特殊性，横纵坐标分别为noclk和clk，auc采用如下方式计算：
<p>1按照pctr聚合 sum_show和sum_clk;
<p>2样本按照pctr排序；
<p>3依次对每个样本，计算noclk和clk围成对小梯形对面积。
<／dependency>
代码见：calcu_AUC_Qdistribution.py



