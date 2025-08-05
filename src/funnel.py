import pandas as pd
from datetime import datetime, timedelta
from config import FUNNEL_STEPS, MEDICAL_CONFIG

class MedicalFunnel:
    def __init__(self, data_path="data/customer_journey.csv"):
        self.df = pd.read_csv(data_path, parse_dates=["timestamp"])
        self.funnel_steps = FUNNEL_STEPS
        
    def calculate_funnel(self, start_date=None, end_date=None):
        """计算基础漏斗转化率"""
        df = self.df.copy()
        
        # 时间筛选
        if start_date:
            df = df[df["timestamp"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["timestamp"] <= pd.to_datetime(end_date)]
        
        # 计算各阶段UV
        funnel_data = []
        for step in self.funnel_steps:
            uv = df[df["event"] == step]["user_id"].nunique()
            funnel_data.append({"step": step, "users": uv})
        
        # 计算转化率
        funnel_df = pd.DataFrame(funnel_data)
        funnel_df["conversion_rate"] = funnel_df["users"] / funnel_df["users"].iloc[0]
        funnel_df["dropoff_rate"] = 1 - funnel_df["conversion_rate"]
        
        return funnel_df
    
    def chronic_disease_funnel(self):
        """慢病患者的特殊漏斗分析"""
        chronic_df = self.df[self.df["is_chronic"] == True]
        
        results = {}
        for disease, drugs in MEDICAL_CONFIG["chronic_disease_drugs"].items():
            disease_users = chronic_df[chronic_df["chronic_type"] == disease]
            funnel_data = []
            
            for step in self.funnel_steps:
                uv = disease_users[disease_users["event"] == step]["user_id"].nunique()
                funnel_data.append({"step": step, "users": uv, "disease": disease})
            
            results[disease] = pd.DataFrame(funnel_data)
        
        return results
    
    def time_based_funnel(self, time_window="7d"):
        """时间维度漏斗分析"""
        df = self.df.copy()
        df["time_group"] = df["timestamp"].dt.to_period(time_window)
        
        funnel_by_time = []
        for period, group in df.groupby("time_group"):
            period_data = []
            for step in self.funnel_steps:
                uv = group[group["event"] == step]["user_id"].nunique()
                period_data.append({"step": step, "users": uv, "period": str(period)})
            
            funnel_by_time.append(pd.DataFrame(period_data))
        
        return pd.concat(funnel_by_time)
    
    def product_funnel(self, top_n=5):
        """药品维度的漏斗分析"""
        top_products = self.df["product"].value_counts().head(top_n).index.tolist()
        
        results = {}
        for product in top_products:
            product_users = self.df[self.df["product"] == product]
            funnel_data = []
            
            for step in self.funnel_steps:
                uv = product_users[product_users["event"] == step]["user_id"].nunique()
                funnel_data.append({"step": step, "users": uv, "product": product})
            
            results[product] = pd.DataFrame(funnel_data)
        
        return results
