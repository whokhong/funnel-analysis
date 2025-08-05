# 漏斗阶段定义 (医药行业典型路径)
FUNNEL_STEPS = [
    "ad_exposure",      # 广告曝光
    "landing_page",     # 落地页访问
    "product_view",     # 商品浏览
    "prescription",     # 电子处方开具（医药关键步骤）
    "cart_add",         # 加入购物车
    "checkout",         # 结算页到达
    "payment",         # 支付完成
    "repurchase"       # 30天内复购（医药行业核心指标）
]

# 医药行业特定参数
MEDICAL_CONFIG = {
    "prescription_required": ["Insulin", "Antibiotics"],  # 需要处方的药品
    "chronic_disease_drugs": {                            # 慢病药品
        "Diabetes": ["Metformin", "Insulin"],
        "Hypertension": ["Lisinopril", "Amlodipine"]
    },
    "funnel_time_window": "30d"  # 漏斗分析时间窗口
}
