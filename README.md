# 基于 Binance API 的加密货币高频/准做市策略（MVP）

> ⚠️ 本项目仅用于研究与教学，不承诺收益，不以制造虚假交易量为目的，禁止自成交（self-trade）/对刷（wash trading）/任何违规行为。请严格遵守 Binance 与所在地法律法规。

## 1. 项目结构

```text
cryptoneozz/
├── .env.example
├── config.yaml
├── data/
│   └── sample_klines.csv
├── requirements.txt
├── README.md
├── src/hfmm/
│   ├── main.py
│   ├── metrics.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── models.py
│   ├── clients/
│   │   └── binance_client.py
│   ├── strategy/
│   │   └── market_maker.py
│   ├── risk/
│   │   └── manager.py
│   ├── engine/
│   │   ├── paper_engine.py
│   │   └── live_engine.py
│   ├── backtest/
│   │   └── engine.py
│   └── utils/
│       └── report.py
└── tests/
    ├── test_metrics.py
    └── test_strategy.py
```

## 2. 功能说明

- **回测模块**：`BacktestEngine`（简化 K 线成交假设，含手续费/返佣估算）。
- **模拟盘模块**：`PaperEngine`（WebSocket 深度 + 成交，dry-run 撮合模拟）。
- **实盘模块**：`LiveEngine`（默认不开启；需手动 `ENABLE_LIVE_TRADING=true`）。
- **风控模块**：
  - 单日最大亏损
  - 单笔最大下单金额
  - 最大净持仓
  - 最大连续亏损次数
  - API 失败熔断
  - 余额不足禁止下单
  - 异常状态可暂停交易
- **统计模块**：`metrics.py`
  - turnover、maker/taker 比例、fee、rebate estimate、gross/net pnl、inventory exposure、fill ratio

## 3. 关键策略逻辑

1. 通过 `mid price=(bid+ask)/2` 在买一卖一附近报价。
2. 点差动态调节：基础点差 + 波动率 + 盘口不平衡 + 成交方向偏置。
3. 小额双边挂单，保持中性库存。
4. 成交后自动更新库存并继续双边报价。
5. 通过库存偏移（inventory skew）降低方向暴露。
6. 当报价异常（`bid >= ask`）时强制拉开，避免潜在自成交。

## 4. 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. 启动

### 5.1 回测
```bash
PYTHONPATH=src python -m hfmm.main --mode backtest
```

### 5.2 模拟盘（默认）
```bash
cp .env.example .env
PYTHONPATH=src python -m hfmm.main --mode paper
```

### 5.3 实盘（默认关闭）
```bash
# 先编辑 .env
# ENABLE_LIVE_TRADING=true
PYTHONPATH=src python -m hfmm.main --mode live
```

## 6. API Key 配置

在 `.env` 中配置：

- `BINANCE_API_KEY`
- `BINANCE_API_SECRET`
- `BASE_URL`（主网默认 `https://api.binance.com`）
- `TESTNET`（建议先 `true`）
- `ENABLE_LIVE_TRADING=false`（默认）

## 7. 重要参数（config.yaml）

- `strategy.base_spread_bps`：基础点差（bps），默认 `4.0`
- `strategy.order_size_usdt`：单次报价名义金额，默认 `30`
- `strategy.order_ttl_sec`：订单超时时间，默认 `12s`
- `risk.max_daily_loss`：日亏损上限，默认 `60 USDT`
- `risk.max_order_notional`：单笔最大下单金额，默认 `50 USDT`
- `risk.max_net_position`：最大净持仓（BTC/ETH 数量），默认 `0.01`
- `fees.maker_fee_bps` / `taker_fee_bps` / `rebate_bps`：手续费与返佣估算参数

## 8. 风险提示

- 回测为简化模型，无法替代真实撮合与排队优先级。
- 高频策略对延迟、网络抖动、交易规则细节极其敏感。
- 不要使用 Martingale（马丁）/无限加仓/无限追单。
- 不承诺收益，实盘前请先长期模拟盘。

## 9. 后续增强方向（增强版路线图）

1. 增加本地订单簿重建（diff depth + checksum）与断线续传。
2. 加入真实订单状态机（new/partially filled/filled/canceled/rejected）。
3. 更精细化库存风险模型（Avellaneda-Stoikov 风格参数化）。
4. 增加异常行情识别（跳价、流动性蒸发）与自动停机。
5. 引入多交易对与资金分配器。
6. 引入 Prometheus/Grafana 监控与告警。
7. 增加 replay 回放回测（tick/depth 级）。
8. 增加 CI、更多单元测试与集成测试。

## 10. 合规声明

本策略目标是提升**有效成交质量与流动性提供能力**，成交量仅用于统计分析，严禁为刷量而进行违规设计。
