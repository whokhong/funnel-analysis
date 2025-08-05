from src.funnel import MedicalFunnel
from src.visualization import plot_funnel, plot_chronic_funnel, plot_time_funnel
from src.medical_features import MedicalFeatureEngineer
import pandas as pd

# 初始化漏斗分析
print("Loading data...")
funnel_analyzer = MedicalFunnel()

# 基础漏斗分析
print("Calculating base funnel...")
base_funnel = funnel_analyzer.calculate_funnel()
plot_funnel(base_funnel, "医药电商整体转化漏斗")

# 慢病患者分析
print("Analyzing chronic patients...")
chronic_results = funnel_analyzer.chronic_disease_funnel()
plot_chronic_funnel(chronic_results)

# 时间维度分析
print("Analyzing time trends...")
time_funnel = funnel_analyzer.time_based_funnel("7d")
plot_time_funnel(time_funnel)

# 特征工程
print("Engineering medical features...")
feature_engineer = MedicalFeatureEngineer(funnel_analyzer.df)
enhanced_df = (feature_engineer
              .add_prescription_features()
              .add_chronic_features()
              .add_funnel_features())

# 保存结果
enhanced_df.to_csv("enhanced_funnel_data.csv", index=False)
print("Analysis results saved to enhanced_funnel_data.csv")
