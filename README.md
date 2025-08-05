安装依赖：pip install -r requirements.txt

生成测试数据：python -c "from src.funnel import generate_customer_journey; generate_customer_journey()"

运行分析：python main.py

ps 
关键价值点:
1.医药场景深度适配：

处方环节特殊处理（30%的漏斗流失发生在处方→支付环节）

慢病患者复购路径单独分析

2.多维度诊断能力：
graph TD
A[整体漏斗] --> B[时间趋势]
A --> C[药品分类]
A --> D[患者类型]
D --> E[慢病患者]
D --> F[普通患者]



业务落地场景：
识别处方流失瓶颈点（优化在线问诊流程）

慢病患者用药周期预测（库存管理）

营销渠道效果评估（广告→处方转化率）
