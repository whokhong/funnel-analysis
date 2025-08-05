import pandas as pd
from config import MEDICAL_CONFIG

class MedicalFeatureEngineer:
    def __init__(self, funnel_df):
        self.df = funnel_df
        
    def add_prescription_features(self):
        """添加处方相关特征"""
        # 是否涉及处方药
        self.df["is_prescription"] = self.df["product"].isin(
            MEDICAL_CONFIG["prescription_required"]
        )
        
        # 处方到支付的延迟时间
        prescription_times = self.df[self.df["event"] == "prescription"].groupby("user_id")["timestamp"].first()
        payment_times = self.df[self.df["event"] == "payment"].groupby("user_id")["timestamp"].first()
        
        delay = (payment_times - prescription_times).dt.total_seconds() / 3600  # 转换为小时
        self.df["prescription_to_payment_hours"] = self.df["user_id"].map(delay)
        
        return self.df
    
    def add_chronic_features(self):
        """添加慢病相关特征"""
        # 慢病药品购买频次
        chronic_drugs = [drug for lst in MEDICAL_CONFIG["chronic_disease_drugs"].values() for drug in lst]
        chronic_users = self.df[self.df["product"].isin(chronic_drugs)]["user_id"].unique()
        
        self.df["is_chronic_user"] = self.df["user_id"].isin(chronic_users)
        
        # 计算慢病用药间隔
        if "is_chronic" in self.df.columns:
            chronic_events = self.df[self.df["is_chronic"]].sort_values(["user_id", "timestamp"])
            chronic_events["time_since_last"] = chronic_events.groupby("user_id")["timestamp"].diff().dt.total_seconds() / 86400  # 转换为天
            self.df = self.df.merge(
                chronic_events[["user_id", "timestamp", "time_since_last"]],
                on=["user_id", "timestamp"],
                how="left"
            )
        
        return self.df
    
    def add_funnel_features(self):
        """添加漏斗阶段特征"""
        # 各阶段时间戳
        events = self.df.pivot(index="user_id", columns="event", values="timestamp").reset_index()
        
        # 计算关键路径时间
        events["awareness_to_prescription"] = (
            events["prescription"] - events["ad_exposure"]
        ).dt.total_seconds() / 3600
        
        events["prescription_to_payment"] = (
            events["payment"] - events["prescription"]
        ).dt.total_seconds() / 3600
        
        self.df = self.df.merge(events, on="user_id", how="left")
        return self.df
