# 火币 WebSocket 行情数据获取示例
# Get bitcoin trading data by websocket in huobi.

主要用于获取数据做量化分析
These data will be used for quant trade research.

整体流程为：
连接 websocket 接口 -> 接收 tick 数据 -> 写入 sqlite，存入数据

This project process：
Connect websocket interface -> Get tick data -> Write data in sqlite



# 后续计划

将方法通用化，希望实现：
1、获取多交易所数据
2、获取多种行情数据，例如：多种时间K线

变成一个通用的行情记录器