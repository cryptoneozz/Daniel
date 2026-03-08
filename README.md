Last login: Sun Mar  8 22:12:42 on ttys000
daniel@DanieldeMacBook-Pro ~ % codex
╭──────────────────────────────────────────────╮
│ >_ OpenAI Codex (v0.111.0)                   │
│                                              │
│ model:     gpt-5.4 medium   /model to change │
│ directory: ~                                 │
╰──────────────────────────────────────────────╯

  Tip: New Try the Codex App with 2x rate limits until April 2nd. Run 'codex ap
  p' or visit https://chatgpt.com/codex?app-landing-page=true


› 你是一名资深 Python 量化开发工程师和加密货币做市策略工程师，请帮我生成一个“基
  于 Binance API 的加密货币高频/准做市策略”完整项目，要求如下：

  一、目标
  - 使用 Python 开发。
  - 交易所：Binance。
  - 策略类型：高频/准做市（不是刷量，不允许自成交，不允许任何违规交易行为）。
  - 初始资金：1000 USDT。
  - 目标是在真实市场环境中尽可能提高有效成交量，并通过点差收益、手续费优化、返
  佣测算来评估策略可行性。
  - 必须强调：不能承诺收益，不能以制造虚假交易量为目的，必须遵守交易所规则并避
  免 self-trade / wash trading。

  二、项目输出要求
  请直接输出一个可运行的 Python 项目，包含：
  1. 项目目录结构
  2. 所有源码文件完整内容
  3. requirements.txt
  4. .env.example
  5. README.md
  6. 风险提示和使用说明
  7. 回测模块
  8. 模拟盘模块
  9. 实盘模块（默认关闭真实下单，需手动开启）

  三、技术要求
  - Python 3.11+
  - 尽量使用：
    - python-binance 或 ccxt（二选一，优先选择更适合 Binance 的方案）
    - asyncio
    - websockets
    - pandas
    - numpy
    - pydantic
    - loguru
  - 配置通过 .env 读取：
    - BINANCE_API_KEY
    - BINANCE_API_SECRET
    - BASE_URL
    - TESTNET 开关
  - 代码风格：
    - 模块化
    - 类型注解完整
    - 关键逻辑有中文注释
    - 有异常处理、重连机制、日志系统

  四、策略逻辑要求
  请实现一个“中性高频做市/挂单捕捉”策略原型：
  - 交易对：先默认 BTCUSDT 或 ETHUSDT，可配置。
  - 使用 WebSocket 订阅：
    - order book 深度
    - 最新成交
    - kline（可选）
  - 核心逻辑：
    1. 根据盘口中间价 mid price 计算买一卖一附近的挂单价格
    2. 动态调整挂单间距（spread），考虑：
       - 波动率
       - 盘口不平衡
       - 最近成交方向
       - 库存风险
    3. 小额双边挂单，尽量提供流动性
    4. 若单边成交后，自动重建另一侧挂单并控制净敞口
    5. 设置最大持仓限制，避免方向暴露过大
    6. 订单超时自动撤单重挂
    7. 限制单次下单数量和总订单数
    8. 防止重复下单、脏数据、网络抖动导致的异常行为
    9. 严格避免可能导致自成交的逻辑

  五、风控要求
  必须实现以下风控：
  - 单日最大亏损限制
  - 单笔最大下单金额限制
  - 最大净持仓限制
  - 最大连续亏损次数限制
  - 最大滑点容忍
  - API 失败熔断
  - WebSocket 断线重连
  - 撤单失败重试
  - 异常行情暂停交易
  - 账户余额不足时禁止下单

  六、成交量与返佣测算
  请单独实现一个统计模块：
  - 统计每日总成交额（turnover）
  - 统计 maker / taker 成交占比
  - 统计手续费支出
  - 统计如果存在返佣时的返佣估算
  - 输出：
    - 总成交额
    - 净 pnl
    - 毛 pnl
    - fee
    - rebate estimate
    - inventory exposure
    - fill ratio
  - 重点说明：成交量目标只能作为统计指标，不能为了刷量而进行违规设计

  七、回测要求
  实现一个简化回测引擎：
  - 输入历史 K 线或逐笔/盘口数据（如果没有逐笔盘口，就基于简化假设）
  - 能模拟挂单成交、撤单、库存变化、手续费
  - 输出回测报告：
    - 总收益
    - 最大回撤
    - Sharpe（简化版）
    - 胜率
    - 成交量
    - 手续费
    - 返佣估算
  - 要明确说明：简化回测不能替代真实撮合环境

  八、实盘安全要求
  - 默认只启动模拟盘 dry-run 模式
  - 必须设置一个明确开关 ENABLE_LIVE_TRADING=false
  - 只有当用户手动改为 true 才允许真实下单
  - 下单前打印风险警告
  - 禁止市价单无限追单
  - 禁止 Martingale、无限加仓、爆仓型逻辑

  九、API 封装要求
  请封装 BinanceClient，至少包括：
  - 获取账户信息
  - 获取余额
  - 获取交易规则
  - 下单
  - 撤单
  - 查询订单
  - 查询持仓
  - WebSocket 行情订阅
  - 自动处理精度、最小下单量、最小名义价值限制

  十、我要的输出格式
  请按以下顺序输出：
  1. 项目结构树
  2. 每个文件的完整代码
  3. 安装命令
  4. 启动命令
  5. 如何切换模拟盘/实盘
  6. 如何配置 API Key
  7. 风险说明
  8. 后续可优化方向

  十一、附加要求
  - 给出一个可运行的最小版本 MVP
  - 再给出一个增强版优化方向列表
  - README 用中文写
  - 对每个重要参数给默认值与解释
  - 增加一个 config.yaml
  - 增加一个 metrics.py 用于统计成交量、手续费、返佣和净收益
  - 增加单元测试样例

  请直接开始生成完整项目代码，不要只给思路，不要省略关键文件。


• 我会先在工作区里建立项目目录，并快速查看可用的风控技能说明，只读取完成这次实现
  所需的最小上下文。

• Ran pwd && rg --files /Users/daniel/.agents/skills/risk-management /Users/
  │ daniel/.agents/skills/trading-plan-generator /Users/daniel/.codex/
  │ skills/.system/skill-creator 2>/dev/null
  └ /Users/daniel
    /Users/daniel/.agents/skills/trading-plan-generator/SKILL.md
    … +15 lines
    /Users/daniel/.codex/skills/.system/skill-creator/agents/openai.yaml
    /Users/daniel/.codex/skills/.system/skill-creator/references/openai_yaml.md

• Explored
  └ List daniel

────────────────────────────────────────────────────────────────────────────────

• 这次会用 risk-management 技能里的风控约束作为参数设计参考，其余部分直接按可运
  行的 Python 项目落地。接下来我先读技能说明，再一次性生成项目骨架和源码。

• Explored
  └ Read SKILL.md

• Ran mkdir -p /Users/daniel/binance_mm_mvp
  └ (no output)

────────────────────────────────────────────────────────────────────────────────

• 我已经确认风控技能里可直接复用的约束主要是单笔风险、交易频率上限和高波动缩仓，
  这些会落到配置和风控模块里。下面按 MVP 可运行标准实现：客户端封装、策略、回
  测、模拟盘、实盘开关、指标统计、配置、测试和中文 README。

• Updated Plan
  └ 按可运行的最小项目一次性生成，再做本地自检。
    □ 设计项目结构与配置模型，明确模块边界和默认参数
    □ 实现 Binance 客户端、WebSocket、策略、风控、指标、回测与运行入口
    □ 补充 README、示例配置、requirements 和单元测试
    □ 运行基础测试与静态启动检查，整理最终输出

• 现在开始落文件。我会先创建目录，再一次性写入核心源码和配置文件，避免中间状态不
  完整。

• Ran mkdir -p /Users/daniel/binance_mm_mvp/binance_mm/clients /Users/daniel/
  │ binance_mm_mvp/binance_mm/strategy /Users/daniel/binance_mm_mvp/
  │ binance_mm/backtest /Users/daniel/binance_mm_mvp/binance_mm/engine /Users/
  │ … +1 lines
  └ (no output)

• Edited 19 files (+1441 -0)
  └ binance_mm_mvp/.env.example (+5 -0)
    1 +BINANCE_API_KEY=your_api_key
    2 +BINANCE_API_SECRET=your_api_secret
    3 +BASE_URL=https://api.binance.com
    4 +TESTNET=true
    5 +ENABLE_LIVE_TRADING=false

  └ binance_mm_mvp/README.md (+149 -0)
      1 +# Binance 高频/准做市策略 MVP
      2 +
      3 +这是一个基于 Binance API 的 Python 3.11+ 高频/准做市策略原型项目，重点
         是：
      4 +
      5 +- 用中性双边挂单提高有效成交概率
      6 +- 用点差收益、手续费、返佣估算评估可行性
      7 +- 默认仅运行回测或模拟盘
      8 +- 严格避免刷量、自成交、违规交易和无限追单
      9 +
     10 +## 免责声明
     11 +
     12 +- 本项目仅用于研究、教学和策略原型验证，不构成任何收益承诺。
     13 +- 成交量只能作为统计指标，不能以制造虚假交易量为目标。
     14 +- 必须遵守 Binance 交易规则，严禁 self-trade / wash trading。
     15 +- 简化回测和模拟盘不能替代真实撮合环境，真实环境存在延迟、排队、拒单、
         滑点、手续费层级变化等风险。
     16 +
     17 +## 主要能力
     18 +
     19 +- `python-binance` REST API 封装
     20 +- `websockets` 行情订阅与断线重连
     21 +- 中性双边挂单策略原型
     22 +- 风控模块：日亏损、单笔名义价值、最大净仓位、连续亏损、滑点、API 熔断
         、异常波动暂停
     23 +- `metrics.py` 统计成交额、maker/taker 占比、手续费、返佣估算、PnL、库
         存暴露、成交率
     24 +- 简化回测引擎
     25 +- 模拟盘与实盘统一执行框架
     26 +- 单元测试样例
     27 +
     28 +## 项目结构
     29 +
     30 +```text
     31 +binance_mm_mvp/
     32 +├── .env.example
     33 +├── README.md
     34 +├── config.yaml
     35 +├── main.py
     36 +├── requirements.txt
     37 +├── binance_mm/
     38 +│   ├── __init__.py
     39 +│   ├── config.py
     40 +│   ├── metrics.py
     41 +│   ├── models.py
     42 +│   ├── risk.py
     43 +│   ├── utils.py
     44 +│   ├── clients/
     45 +│   │   └── binance_client.py
     46 +│   ├── strategy/
     47 +│   │   └── market_maker.py
     48 +│   ├── engine/
     49 +│   │   ├── live_trader.py
     50 +│   │   └── simulator.py
     51 +│   ├── backtest/
     52 +│   │   └── engine.py
     53 +│   └── data/
     54 +│       └── sample_klines.csv
     55 +└── tests/
     56 +    ├── test_metrics.py
     57 +    └── test_risk.py
     58 +```
     59 +
     60 +## 重要参数默认值与解释
     61 +
     62 +- `app.symbol=BTCUSDT`：默认交易对，可改为 `ETHUSDT`
     63 +- `app.initial_cash=1000`：默认初始资金，仅用于回测/模拟盘初始化
     64 +- `app.enable_live_trading=false`：默认禁止实盘
     65 +- `strategy.base_spread_bps=6`：基础挂单点差
     66 +- `strategy.order_size_usdt=50`：每次双边挂单的单边名义价值
     67 +- `strategy.max_total_orders=2`：最多保留 1 买 1 卖
     68 +- `risk.max_daily_loss=50`：当日最大亏损限制
     69 +- `risk.max_order_notional=100`：单笔最大下单金额
     70 +- `risk.max_net_position_base=0.01`：最大净持仓，BTC 下约为 0.01 BTC
     71 +- `risk.max_consecutive_losses=4`：最大连续亏损次数
     72 +- `risk.abnormal_volatility_bps=40`：异常波动阈值，超过后暂停交易
     73 +- `fees.maker_fee_bps=1` / `fees.taker_fee_bps=3.5`：默认费率，可按账户
         等级调整
     74 +- `fees.rebate_bps=0.2`：返佣估算值，仅用于统计模拟
     75 +
     76 +## 安装
     77 +
     78 +```bash
     79 +cd /Users/daniel/binance_mm_mvp
     80 +python3.11 -m venv .venv
     81 +source .venv/bin/activate
     82 +pip install -r requirements.txt
     83 +cp .env.example .env
     84 +```
     85 +
     86 +## 启动
     87 +
     88 +### 1. 回测
     89 +
     90 +```bash
     91 +python main.py --mode backtest
     92 +```
     93 +
     94 +### 2. 模拟盘
     95 +
     96 +```bash
     97 +python main.py --mode paper
     98 +```
     99 +
    100 +### 3. 实盘
    101 +
    102 +先修改 `.env` 与 `config.yaml`：
    103 +
    104 +- `.env` 中设置真实 API Key
    105 +- `ENABLE_LIVE_TRADING=true`
    106 +- `config.yaml` 中 `app.enable_live_trading: true`
    107 +- `app.testnet: false` 或按需切换 Binance Spot Testnet
    108 +
    109 +然后执行：
    110 +
    111 +```bash
    112 +python main.py --mode live
    113 +```
    114 +
    115 +## 模拟盘/实盘切换
    116 +
    117 +- 模拟盘：`--mode paper`，且 `ENABLE_LIVE_TRADING=false`
    118 +- 实盘：`--mode live`，同时 `.env` 与 `config.yaml` 中的实盘开关都必须
         为 `true`
    119 +
    120 +双重开关的目的是降低误下单风险。
    121 +
    122 +## API Key 配置
    123 +
    124 +在 `.env` 中配置：
    125 +
    126 +```env
    127 +BINANCE_API_KEY=你的_API_KEY
    128 +BINANCE_API_SECRET=你的_API_SECRET
    129 +BASE_URL=https://api.binance.com
    130 +TESTNET=true
    131 +ENABLE_LIVE_TRADING=false
    132 +```
    133 +
    134 +## 风险说明
    135 +
    136 +- 禁止使用 Martingale、无限补仓、无限追价。
    137 +- 默认仅限价单，不做市价单无限追单。
    138 +- 策略包含自成交保护：只保留一个买单和一个卖单，且报价始终严格低于卖价
         、高于买价。
    139 +- 若余额不足、API 连续失败、波动异常、日亏损超限，将自动暂停交易。
    140 +- 回测结果仅供参考，不能视为真实收益预期。
    141 +
    142 +## 后续优化方向
    143 +
    144 +1. 接入更高质量的本地 order book 缓存和增量深度校验。
    145 +2. 增加订单队列位置估计、部分成交建模和真实 maker 排队逻辑。
    146 +3. 增加 inventory alpha、中短期趋势过滤和交易时段过滤。
    147 +4. 按账户 VIP 等级动态更新实际手续费与返佣。
    148 +5. 增加 Prometheus/Grafana 监控、SQLite/Parquet 持久化和告警。
    149 +6. 引入多交易对组合和统一风险预算。

  └ binance_mm_mvp/binance_mm/__init__.py (+6 -0)
    1 +__all__ = [
    2 +    "config",
    3 +    "metrics",
    4 +    "models",
    5 +    "risk",
    6 +]

  └ binance_mm_mvp/binance_mm/backtest/engine.py (+154 -0)
      1 +from __future__ import annotations
      2 +
      3 +from pathlib import Path
      4 +
      5 +import numpy as np
      6 +import pandas as pd
      7 +
      8 +from binance_mm.config import Settings
      9 +from binance_mm.metrics import MetricsTracker
     10 +from binance_mm.models import BacktestReport, FillEvent, MarketSnapshot
         , OrderRequest
     11 +from binance_mm.risk import RiskManager
     12 +from binance_mm.strategy.market_maker import MarketMakerStrategy
     13 +from binance_mm.utils import generate_client_order_id
     14 +
     15 +
     16 +class BacktestEngine:
     17 +    def __init__(self, settings: Settings) -> None:
     18 +        self.settings = settings
     19 +        self.metrics = MetricsTracker()
     20 +        self.risk = RiskManager(settings.risk)
     21 +        self.strategy = MarketMakerStrategy(settings)
     22 +        self.open_orders: dict[str, OrderRequest] = {}
     23 +        self.sequence = 0
     24 +        self.cash = settings.app.initial_cash
     25 +        self.base_position = 0.0
     26 +
     27 +    def run(self) -> BacktestReport:
     28 +        df = self._load_data()
     29 +        equity_curve: list[float] = []
     30 +        trade_pnls: list[float] = []
     31 +
     32 +        for _, row in df.iterrows():
     33 +            mid = float(row["close"])
     34 +            synthetic_spread = max(self.settings.strategy.min_spread_bp
         s, 3.0)
     35 +            best_bid = mid * (1 - synthetic_spread / 20_000)
     36 +            best_ask = mid * (1 + synthetic_spread / 20_000)
     37 +            snapshot = MarketSnapshot(
     38 +                symbol=self.settings.app.symbol,
     39 +                best_bid=best_bid,
     40 +                best_ask=best_ask,
     41 +                bid_qty=max(float(row["volume"]) * 0.01, 0.01),
     42 +                ask_qty=max(float(row["volume"]) * 0.01, 0.01),
     43 +                last_trade_price=mid,
     44 +                last_trade_side="BUY" if row["close"] >= row["open"] el
         se "SELL",
     45 +            )
     46 +            self._match_orders(snapshot, float(row["high"]), float(row[
         "low"]), trade_pnls)
     47 +
     48 +            gate = self.risk.allow_trading(self.metrics, snapshot, self
         .cash)
     49 +            if gate.allowed:
     50 +                quote = self.strategy.build_quotes(snapshot, self.metri
         cs)
     51 +                buy_order = OrderRequest(
     52 +                    symbol=snapshot.symbol,
     53 +                    side="BUY",
     54 +                    price=quote.bid_price,
     55 +                    quantity=quote.bid_quantity,
     56 +                    client_order_id=self._next_id("BUY"),
     57 +                )
     58 +                sell_order = OrderRequest(
     59 +                    symbol=snapshot.symbol,
     60 +                    side="SELL",
     61 +                    price=quote.ask_price,
     62 +                    quantity=quote.ask_quantity,
     63 +                    client_order_id=self._next_id("SELL"),
     64 +                )
     65 +                for order in (buy_order, sell_order):
     66 +                    decision = self.risk.validate_order(
     67 +                        order=order,
     68 +                        metrics=self.metrics,
     69 +                        free_usdt=self.cash,
     70 +                        best_bid=snapshot.best_bid,
     71 +                        best_ask=snapshot.best_ask,
     72 +                    )
     73 +                    if decision.allowed:
     74 +                        self.open_orders[order.client_order_id] = order
     75 +                        self.metrics.record_order_submission()
     76 +
     77 +            equity_curve.append(self._mark_equity(mid))
     78 +
     79 +        max_drawdown = self._max_drawdown(equity_curve)
     80 +        returns = np.diff(equity_curve) if len(equity_curve) > 1 else n
         p.array([0.0])
     81 +        sharpe = float(np.mean(returns) / np.std(returns)) if len(retur
         ns) > 1 and np.std(returns) > 0 else 0.0
     82 +        wins = sum(1 for pnl in trade_pnls if pnl > 0)
     83 +        summary = self.metrics.summary(df["close"].iloc[-1])
     84 +
     85 +        return BacktestReport(
     86 +            total_return=(equity_curve[-1] - self.settings.app.initial_
         cash) / self.settings.app.initial_cash if equity_curve else 0.0,
     87 +            max_drawdown=max_drawdown,
     88 +            sharpe=sharpe,
     89 +            win_rate=wins / len(trade_pnls) if trade_pnls else 0.0,
     90 +            turnover=summary.turnover,
     91 +            fees=summary.fees,
     92 +            rebate_estimate=summary.rebate_estimate,
     93 +            gross_pnl=summary.gross_pnl,
     94 +            net_pnl=summary.net_pnl,
     95 +            total_trades=summary.total_fills,
     96 +        )
     97 +
     98 +    def _load_data(self) -> pd.DataFrame:
     99 +        path = Path(self.settings.backtest.data_path)
    100 +        if not path.is_absolute():
    101 +            path = Path(__file__).resolve().parents[2] / self.settings.
         backtest.data_path
    102 +        return pd.read_csv(path)
    103 +
    104 +    def _match_orders(self, snapshot: MarketSnapshot, candle_high: floa
         t, candle_low: float, trade_pnls: list[float]) -> None:
    105 +        for order_id, order in list(self.open_orders.items()):
    106 +            touched = candle_low <= order.price <= candle_high
    107 +            if not touched:
    108 +                continue
    109 +            fill = FillEvent(
    110 +                symbol=order.symbol,
    111 +                side=order.side,
    112 +                price=order.price,
    113 +                quantity=order.quantity,
    114 +                liquidity="maker",
    115 +                fee_bps=self.settings.fees.maker_fee_bps,
    116 +                rebate_bps=self.settings.fees.rebate_bps,
    117 +                order_id=order.client_order_id,
    118 +            )
    119 +            pre_net = self.metrics.summary(snapshot.mid_price).net_pnl
    120 +            self.metrics.record_fill(fill)
    121 +            self._apply_fill(fill)
    122 +            post_net = self.metrics.summary(snapshot.mid_price).net_pnl
    123 +            trade_pnls.append(post_net - pre_net)
    124 +            self.risk.register_trade_result(post_net - pre_net)
    125 +            self.open_orders.pop(order_id, None)
    126 +
    127 +    def _apply_fill(self, fill: FillEvent) -> None:
    128 +        if fill.side == "BUY":
    129 +            self.cash -= fill.notional
    130 +            self.base_position += fill.quantity
    131 +        else:
    132 +            self.cash += fill.notional
    133 +            self.base_position -= fill.quantity
    134 +
    135 +    def _mark_equity(self, mid_price: float) -> float:
    136 +        inventory_value = self.base_position * mid_price
    137 +        net = self.cash + inventory_value - self.metrics.fees + self.me
         trics.rebate_estimate
    138 +        self.metrics.mark_equity(mid_price)
    139 +        return net
    140 +
    141 +    def _max_drawdown(self, values: list[float]) -> float:
    142 +        if not values:
    143 +            return 0.0
    144 +        peak = values[0]
    145 +        max_dd = 0.0
    146 +        for value in values:
    147 +            peak = max(peak, value)
    148 +            if peak > 0:
    149 +                max_dd = max(max_dd, (peak - value) / peak)
    150 +        return max_dd
    151 +
    152 +    def _next_id(self, side: str) -> str:
    153 +        self.sequence += 1
    154 +        return generate_client_order_id("bt", side, self.sequence)

  └ binance_mm_mvp/binance_mm/clients/binance_client.py (+133 -0)
      1 +from __future__ import annotations
      2 +
      3 +from typing import Any
      4 +
      5 +from loguru import logger
      6 +
      7 +from binance_mm.config import Settings
      8 +from binance_mm.models import ManagedOrder, OrderRequest
      9 +from binance_mm.utils import round_step, round_tick
     10 +
     11 +try:
     12 +    from binance import AsyncClient
     13 +except ImportError:  # pragma: no cover
     14 +    AsyncClient = None  # type: ignore[assignment]
     15 +
     16 +
     17 +class BinanceClient:
     18 +    def __init__(self, settings: Settings) -> None:
     19 +        self.settings = settings
     20 +        self.client: AsyncClient | None = None
     21 +        self._exchange_info_cache: dict[str, Any] = {}
     22 +
     23 +    async def connect(self) -> None:
     24 +        if AsyncClient is None:
     25 +            raise RuntimeError("未安装 python-binance，无法连接 Binance
         ")
     26 +        self.client = await AsyncClient.create(
     27 +            api_key=self.settings.binance_api_key,
     28 +            api_secret=self.settings.binance_api_secret,
     29 +            testnet=self.settings.app.testnet,
     30 +        )
     31 +        if self.settings.base_url:
     32 +            self.client.API_URL = self.settings.base_url
     33 +        logger.info("Binance REST 客户端已连接, testnet={}", self.setti
         ngs.app.testnet)
     34 +
     35 +    async def close(self) -> None:
     36 +        if self.client:
     37 +            await self.client.close_connection()
     38 +            self.client = None
     39 +
     40 +    async def get_account_info(self) -> dict[str, Any]:
     41 +        self._assert_client()
     42 +        return await self.client.get_account()
     43 +
     44 +    async def get_balance(self, asset: str) -> float:
     45 +        self._assert_client()
     46 +        account = await self.client.get_account()
     47 +        for balance in account.get("balances", []):
     48 +            if balance["asset"] == asset:
     49 +                return float(balance["free"])
     50 +        return 0.0
     51 +
     52 +    async def get_position(self, asset: str) -> float:
     53 +        return await self.get_balance(asset)
     54 +
     55 +    async def get_symbol_rules(self, symbol: str) -> dict[str, float]:
     56 +        if symbol in self._exchange_info_cache:
     57 +            return self._exchange_info_cache[symbol]
     58 +        self._assert_client()
     59 +        info = await self.client.get_symbol_info(symbol)
     60 +        if not info:
     61 +            raise ValueError(f"未找到交易规则: {symbol}")
     62 +        filters = {item["filterType"]: item for item in info["filters"]
         }
     63 +        rules = {
     64 +            "tick_size": float(filters["PRICE_FILTER"]["tickSize"]),
     65 +            "step_size": float(filters["LOT_SIZE"]["stepSize"]),
     66 +            "min_qty": float(filters["LOT_SIZE"]["minQty"]),
     67 +            "min_notional": float(filters.get("NOTIONAL", filters.get("
         MIN_NOTIONAL", {})).get("minNotional", 0.0)),
     68 +        }
     69 +        self._exchange_info_cache[symbol] = rules
     70 +        return rules
     71 +
     72 +    async def normalize_order(self, order: OrderRequest) -> OrderReques
         t:
     73 +        rules = await self.get_symbol_rules(order.symbol)
     74 +        price = round_tick(order.price, rules["tick_size"])
     75 +        quantity = max(round_step(order.quantity, rules["step_size"]),
         rules["min_qty"])
     76 +        if price * quantity < rules["min_notional"]:
     77 +            quantity = round_step((rules["min_notional"] / max(price, 1
         e-12)) * 1.01, rules["step_size"])
     78 +        return OrderRequest(
     79 +            symbol=order.symbol,
     80 +            side=order.side,
     81 +            price=price,
     82 +            quantity=quantity,
     83 +            client_order_id=order.client_order_id,
     84 +            post_only=order.post_only,
     85 +        )
     86 +
     87 +    async def place_limit_order(self, order: OrderRequest) -> ManagedOr
         der:
     88 +        self._assert_client()
     89 +        normalized = await self.normalize_order(order)
     90 +        params = {
     91 +            "symbol": normalized.symbol,
     92 +            "side": normalized.side,
     93 +            "type": "LIMIT_MAKER" if normalized.post_only else "LIMIT",
     94 +            "timeInForce": "GTC",
     95 +            "price": f"{normalized.price:.8f}",
     96 +            "quantity": f"{normalized.quantity:.8f}",
     97 +            "newClientOrderId": normalized.client_order_id,
     98 +        }
     99 +        response = await self.client.create_order(**params)
    100 +        logger.info("下单成功: {}", response)
    101 +        return ManagedOrder(
    102 +            symbol=normalized.symbol,
    103 +            side=normalized.side,
    104 +            price=normalized.price,
    105 +            quantity=normalized.quantity,
    106 +            client_order_id=normalized.client_order_id,
    107 +            exchange_order_id=response.get("orderId"),
    108 +            status=response.get("status", "NEW"),
    109 +        )
    110 +
    111 +    async def cancel_order(self, symbol: str, order_id: int | None = No
         ne, client_order_id: str | None = None) -> dict[str, Any]:
    112 +        self._assert_client()
    113 +        params: dict[str, Any] = {"symbol": symbol}
    114 +        if order_id is not None:
    115 +            params["orderId"] = order_id
    116 +        if client_order_id is not None:
    117 +            params["origClientOrderId"] = client_order_id
    118 +        result = await self.client.cancel_order(**params)
    119 +        logger.info("撤单结果: {}", result)
    120 +        return result
    121 +
    122 +    async def get_order(self, symbol: str, order_id: int | None = None,
          client_order_id: str | None = None) -> dict[str, Any]:
    123 +        self._assert_client()
    124 +        params: dict[str, Any] = {"symbol": symbol}
    125 +        if order_id is not None:
    126 +            params["orderId"] = order_id
    127 +        if client_order_id is not None:
    128 +            params["origClientOrderId"] = client_order_id
    129 +        return await self.client.get_order(**params)
    130 +
    131 +    def _assert_client(self) -> None:
    132 +        if self.client is None:
    133 +            raise RuntimeError("BinanceClient 尚未 connect()")

  └ binance_mm_mvp/binance_mm/config.py (+113 -0)
      1 +from __future__ import annotations
      2 +
      3 +from pathlib import Path
      4 +from typing import Any
      5 +
      6 +import yaml
      7 +from dotenv import load_dotenv
      8 +from pydantic import BaseModel, ConfigDict, Field
      9 +
     10 +from binance_mm.utils import env_bool, getenv_str
     11 +
     12 +
     13 +class AppConfig(BaseModel):
     14 +    model_config = ConfigDict(extra="ignore")
     15 +
     16 +    name: str = "binance-mm-mvp"
     17 +    mode: str = "paper"
     18 +    symbol: str = "BTCUSDT"
     19 +    quote_asset: str = "USDT"
     20 +    base_asset: str = "BTC"
     21 +    kline_interval: str = "1m"
     22 +    initial_cash: float = 1000.0
     23 +    testnet: bool = True
     24 +    enable_live_trading: bool = False
     25 +    order_refresh_seconds: int = 8
     26 +    stale_data_seconds: int = 5
     27 +    loop_interval_seconds: float = 1.0
     28 +
     29 +
     30 +class StrategyConfig(BaseModel):
     31 +    model_config = ConfigDict(extra="ignore")
     32 +
     33 +    base_spread_bps: float = 6.0
     34 +    min_spread_bps: float = 4.0
     35 +    max_spread_bps: float = 25.0
     36 +    order_size_usdt: float = 50.0
     37 +    max_total_orders: int = 2
     38 +    max_order_age_seconds: int = 12
     39 +    inventory_target_base: float = 0.0
     40 +    inventory_skew_bps_per_unit: float = 12.0
     41 +    volatility_window: int = 60
     42 +    volatility_spread_multiplier: float = 1800.0
     43 +    imbalance_spread_multiplier: float = 8.0
     44 +    trade_bias_spread_multiplier: float = 6.0
     45 +    requote_threshold_bps: float = 3.0
     46 +
     47 +
     48 +class RiskConfig(BaseModel):
     49 +    model_config = ConfigDict(extra="ignore")
     50 +
     51 +    max_daily_loss: float = 50.0
     52 +    max_order_notional: float = 100.0
     53 +    max_net_position_base: float = 0.01
     54 +    max_consecutive_losses: int = 4
     55 +    max_slippage_bps: float = 8.0
     56 +    api_failure_circuit_breaker: int = 5
     57 +    cancel_retry_count: int = 3
     58 +    abnormal_volatility_bps: float = 40.0
     59 +    min_free_usdt: float = 50.0
     60 +
     61 +
     62 +class FeeConfig(BaseModel):
     63 +    model_config = ConfigDict(extra="ignore")
     64 +
     65 +    maker_fee_bps: float = 1.0
     66 +    taker_fee_bps: float = 3.5
     67 +    rebate_bps: float = 0.2
     68 +
     69 +
     70 +class BacktestConfig(BaseModel):
     71 +    model_config = ConfigDict(extra="ignore")
     72 +
     73 +    data_path: str = "binance_mm/data/sample_klines.csv"
     74 +    assume_fill_on_touch: bool = True
     75 +    random_seed: int = 7
     76 +
     77 +
     78 +class Settings(BaseModel):
     79 +    model_config = ConfigDict(extra="ignore")
     80 +
     81 +    app: AppConfig = Field(default_factory=AppConfig)
     82 +    strategy: StrategyConfig = Field(default_factory=StrategyConfig)
     83 +    risk: RiskConfig = Field(default_factory=RiskConfig)
     84 +    fees: FeeConfig = Field(default_factory=FeeConfig)
     85 +    backtest: BacktestConfig = Field(default_factory=BacktestConfig)
     86 +    binance_api_key: str = ""
     87 +    binance_api_secret: str = ""
     88 +    base_url: str = "https://api.binance.com"
     89 +
     90 +
     91 +def _read_yaml(path: Path) -> dict[str, Any]:
     92 +    if not path.exists():
     93 +        return {}
     94 +    with path.open("r", encoding="utf-8") as fh:
     95 +        data = yaml.safe_load(fh) or {}
     96 +    if not isinstance(data, dict):
     97 +        raise ValueError(f"配置文件格式错误: {path}")
     98 +    return data
     99 +
    100 +
    101 +def load_settings(config_path: str = "config.yaml", env_path: str = ".e
         nv") -> Settings:
    102 +    load_dotenv(env_path, override=False)
    103 +    config_data = _read_yaml(Path(config_path))
    104 +
    105 +    settings = Settings(
    106 +        **config_data,
    107 +        binance_api_key=getenv_str("BINANCE_API_KEY", ""),
    108 +        binance_api_secret=getenv_str("BINANCE_API_SECRET", ""),
    109 +        base_url=getenv_str("BASE_URL", "https://api.binance.com"),
    110 +    )
    111 +    settings.app.testnet = env_bool("TESTNET", settings.app.testnet)
    112 +    settings.app.enable_live_trading = env_bool("ENABLE_LIVE_TRADING",
         settings.app.enable_live_trading)
    113 +    return settings

  └ binance_mm_mvp/binance_mm/data/sample_klines.csv (+16 -0)
     1 +open_time,open,high,low,close,volume
     2 +2026-03-01 00:00:00,62000,62040,61960,62010,120.4
     3 +2026-03-01 00:01:00,62010,62055,61990,62030,132.8
     4 +2026-03-01 00:02:00,62030,62080,62010,62020,118.6
     5 +2026-03-01 00:03:00,62020,62100,62000,62085,165.1
     6 +2026-03-01 00:04:00,62085,62110,62050,62070,109.2
     7 +2026-03-01 00:05:00,62070,62160,62040,62140,172.5
     8 +2026-03-01 00:06:00,62140,62170,62090,62105,141.0
     9 +2026-03-01 00:07:00,62105,62140,62030,62060,154.9
    10 +2026-03-01 00:08:00,62060,62090,62010,62020,127.4
    11 +2026-03-01 00:09:00,62020,62075,61980,62040,136.8
    12 +2026-03-01 00:10:00,62040,62120,62010,62110,188.3
    13 +2026-03-01 00:11:00,62110,62140,62090,62120,95.0
    14 +2026-03-01 00:12:00,62120,62185,62080,62160,146.2
    15 +2026-03-01 00:13:00,62160,62220,62110,62130,152.7
    16 +2026-03-01 00:14:00,62130,62150,62070,62095,129.5

  └ binance_mm_mvp/binance_mm/engine/live_trader.py (+222 -0)
      1 +from __future__ import annotations
      2 +
      3 +import asyncio
      4 +import contextlib
      5 +import json
      6 +from collections.abc import AsyncIterator
      7 +
      8 +import websockets
      9 +from loguru import logger
     10 +
     11 +from binance_mm.clients.binance_client import BinanceClient
     12 +from binance_mm.config import Settings
     13 +from binance_mm.engine.simulator import SimulatedExchange
     14 +from binance_mm.metrics import MetricsTracker
     15 +from binance_mm.models import ManagedOrder, MarketSnapshot, OrderReques
         t
     16 +from binance_mm.risk import RiskManager
     17 +from binance_mm.strategy.market_maker import MarketMakerStrategy
     18 +from binance_mm.utils import generate_client_order_id
     19 +
     20 +
     21 +class MarketDataStream:
     22 +    def __init__(self, settings: Settings) -> None:
     23 +        self.settings = settings
     24 +
     25 +    async def stream(self) -> AsyncIterator[MarketSnapshot]:
     26 +        symbol = self.settings.app.symbol.lower()
     27 +        kline_interval = self.settings.app.kline_interval
     28 +        stream_url = (
     29 +            f"wss://stream.binance.com:9443/stream?streams="
     30 +            f"{symbol}@depth5@100ms/{symbol}@trade/{symbol}@kline_{klin
         e_interval}"
     31 +        )
     32 +        if self.settings.app.testnet:
     33 +            stream_url = (
     34 +                f"wss://stream.testnet.binance.vision/stream?streams="
     35 +                f"{symbol}@depth5@100ms/{symbol}@trade/{symbol}@kline_{
         kline_interval}"
     36 +            )
     37 +
     38 +        trade_side = "BUY"
     39 +        last_trade_price = 0.0
     40 +        best_bid = best_ask = bid_qty = ask_qty = 0.0
     41 +        while True:
     42 +            try:
     43 +                async with websockets.connect(stream_url, ping_interval
         =20, ping_timeout=20) as ws:
     44 +                    logger.info("WebSocket 已连接: {}", stream_url)
     45 +                    async for raw in ws:
     46 +                        payload = json.loads(raw)
     47 +                        data = payload.get("data", {})
     48 +                        stream_name = payload.get("stream", "")
     49 +                        if "@trade" in stream_name:
     50 +                            last_trade_price = float(data["p"])
     51 +                            trade_side = "SELL" if data.get("m", False)
          else "BUY"
     52 +                        elif "@depth" in stream_name:
     53 +                            bids = data.get("b", [])
     54 +                            asks = data.get("a", [])
     55 +                            if bids:
     56 +                                best_bid, bid_qty = float(bids[0][0]),
         float(bids[0][1])
     57 +                            if asks:
     58 +                                best_ask, ask_qty = float(asks[0][0]),
         float(asks[0][1])
     59 +                        if best_bid > 0 and best_ask > 0:
     60 +                            yield MarketSnapshot(
     61 +                                symbol=self.settings.app.symbol,
     62 +                                best_bid=best_bid,
     63 +                                best_ask=best_ask,
     64 +                                bid_qty=bid_qty,
     65 +                                ask_qty=ask_qty,
     66 +                                last_trade_price=last_trade_price or (b
         est_bid + best_ask) / 2.0,
     67 +                                last_trade_side=trade_side,
     68 +                            )
     69 +            except Exception as exc:  # pragma: no cover
     70 +                logger.warning("WebSocket 异常，准备重连: {}", exc)
     71 +                await asyncio.sleep(2)
     72 +
     73 +
     74 +class LiveTrader:
     75 +    def __init__(self, settings: Settings, mode: str = "paper") -> None
         :
     76 +        self.settings = settings
     77 +        self.mode = mode
     78 +        self.metrics = MetricsTracker()
     79 +        self.risk = RiskManager(settings.risk)
     80 +        self.strategy = MarketMakerStrategy(settings)
     81 +        self.ws = MarketDataStream(settings)
     82 +        self.sequence = 0
     83 +        self.last_snapshot: MarketSnapshot | None = None
     84 +        self.last_quote: tuple[float, float] | None = None
     85 +        self.open_orders: dict[str, ManagedOrder] = {}
     86 +        self.paper_exchange = SimulatedExchange(settings, self.metrics)
     87 +        self.binance_client = BinanceClient(settings)
     88 +
     89 +    async def run(self) -> None:
     90 +        if self.mode == "live":
     91 +            self._ensure_live_enabled()
     92 +            logger.warning("实盘模式已开启。下单前请再次确认风险、费率
         、权限与账户余额。")
     93 +            await self.binance_client.connect()
     94 +        try:
     95 +            async for snapshot in self.ws.stream():
     96 +                self.last_snapshot = snapshot
     97 +                await self._on_snapshot(snapshot)
     98 +        finally:
     99 +            await self._cleanup()
    100 +
    101 +    async def _on_snapshot(self, snapshot: MarketSnapshot) -> None:
    102 +        free_usdt = self.paper_exchange.balances.free_quote
    103 +        if self.mode == "live":
    104 +            try:
    105 +                free_usdt = await self.binance_client.get_balance(self.
         settings.app.quote_asset)
    106 +                self.risk.register_api_success()
    107 +            except Exception as exc:  # pragma: no cover
    108 +                self.risk.register_api_failure()
    109 +                logger.error("获取余额失败: {}", exc)
    110 +                return
    111 +
    112 +        gate = self.risk.allow_trading(self.metrics, snapshot, free_usd
         t)
    113 +        if not gate.allowed:
    114 +            logger.warning("暂停交易: {}", gate.reason)
    115 +            await self._cancel_stale(force_all=True)
    116 +            return
    117 +
    118 +        fills = self.paper_exchange.process_snapshot(snapshot) if self.
         mode == "paper" else []
    119 +        for fill in fills:
    120 +            logger.info("模拟成交: {}", fill)
    121 +
    122 +        await self._cancel_stale(force_all=False)
    123 +        quote = self.strategy.build_quotes(snapshot, self.metrics)
    124 +        if not self._should_requote(quote.bid_price, quote.ask_price):
    125 +            return
    126 +
    127 +        await self._replace_quotes(snapshot, free_usdt)
    128 +        summary = self.metrics.summary(snapshot.mid_price)
    129 +        logger.info("metrics={}", summary)
    130 +
    131 +    async def _replace_quotes(self, snapshot: MarketSnapshot, free_usdt
         : float) -> None:
    132 +        quote = self.strategy.build_quotes(snapshot, self.metrics)
    133 +        await self._cancel_stale(force_all=True)
    134 +
    135 +        orders = [
    136 +            OrderRequest(
    137 +                symbol=snapshot.symbol,
    138 +                side="BUY",
    139 +                price=quote.bid_price,
    140 +                quantity=quote.bid_quantity,
    141 +                client_order_id=self._next_client_order_id("BUY"),
    142 +            ),
    143 +            OrderRequest(
    144 +                symbol=snapshot.symbol,
    145 +                side="SELL",
    146 +                price=quote.ask_price,
    147 +                quantity=quote.ask_quantity,
    148 +                client_order_id=self._next_client_order_id("SELL"),
    149 +            ),
    150 +        ]
    151 +
    152 +        for order in orders:
    153 +            if len(self.open_orders) >= self.settings.strategy.max_tota
         l_orders:
    154 +                break
    155 +            decision = self.risk.validate_order(
    156 +                order=order,
    157 +                metrics=self.metrics,
    158 +                free_usdt=free_usdt,
    159 +                best_bid=snapshot.best_bid,
    160 +                best_ask=snapshot.best_ask,
    161 +            )
    162 +            if not decision.allowed:
    163 +                logger.warning("订单被风控拒绝 {}: {}", order.client_or
         der_id, decision.reason)
    164 +                continue
    165 +            if self.mode == "paper":
    166 +                managed = self.paper_exchange.place_order(order)
    167 +            else:
    168 +                try:
    169 +                    managed = await self.binance_client.place_limit_ord
         er(order)
    170 +                    self.risk.register_api_success()
    171 +                except Exception as exc:  # pragma: no cover
    172 +                    self.risk.register_api_failure()
    173 +                    logger.error("实盘下单失败: {}", exc)
    174 +                    continue
    175 +            self.open_orders[managed.client_order_id] = managed
    176 +        self.last_quote = (quote.bid_price, quote.ask_price)
    177 +
    178 +    async def _cancel_stale(self, force_all: bool) -> None:
    179 +        for client_order_id, order in list(self.open_orders.items()):
    180 +            if not force_all and order.age_seconds < self.settings.stra
         tegy.max_order_age_seconds:
    181 +                continue
    182 +            if self.mode == "paper":
    183 +                self.paper_exchange.cancel_order(client_order_id)
    184 +            else:
    185 +                for attempt in range(self.settings.risk.cancel_retry_co
         unt):
    186 +                    try:
    187 +                        await self.binance_client.cancel_order(
    188 +                            symbol=order.symbol,
    189 +                            order_id=order.exchange_order_id,
    190 +                            client_order_id=order.client_order_id,
    191 +                        )
    192 +                        self.risk.register_api_success()
    193 +                        break
    194 +                    except Exception as exc:  # pragma: no cover
    195 +                        self.risk.register_api_failure()
    196 +                        logger.warning("撤单失败 attempt={} error={}",
         attempt + 1, exc)
    197 +                        await asyncio.sleep(0.5)
    198 +            self.open_orders.pop(client_order_id, None)
    199 +
    200 +    def _should_requote(self, bid_price: float, ask_price: float) -> bo
         ol:
    201 +        if self.last_quote is None:
    202 +            return True
    203 +        old_bid, old_ask = self.last_quote
    204 +        if old_bid <= 0 or old_ask <= 0:
    205 +            return True
    206 +        diff_bid_bps = abs(bid_price - old_bid) / old_bid * 10_000
    207 +        diff_ask_bps = abs(ask_price - old_ask) / old_ask * 10_000
    208 +        return max(diff_bid_bps, diff_ask_bps) >= self.settings.strateg
         y.requote_threshold_bps
    209 +
    210 +    def _next_client_order_id(self, side: str) -> str:
    211 +        self.sequence += 1
    212 +        return generate_client_order_id("mm", side, self.sequence)
    213 +
    214 +    def _ensure_live_enabled(self) -> None:
    215 +        if not self.settings.app.enable_live_trading:
    216 +            raise RuntimeError("实盘模式被禁用。请先将 ENABLE_LIVE_TRAD
         ING 与 config.yaml 中开关都设为 true。")
    217 +
    218 +    async def _cleanup(self) -> None:
    219 +        with contextlib.suppress(Exception):
    220 +            await self._cancel_stale(force_all=True)
    221 +        with contextlib.suppress(Exception):
    222 +            await self.binance_client.close()

  └ binance_mm_mvp/binance_mm/engine/simulator.py (+79 -0)
     1 +from __future__ import annotations
     2 +
     3 +from dataclasses import dataclass
     4 +
     5 +from loguru import logger
     6 +
     7 +from binance_mm.config import Settings
     8 +from binance_mm.metrics import MetricsTracker
     9 +from binance_mm.models import FillEvent, ManagedOrder, MarketSnapshot, O
        rderRequest
    10 +
    11 +
    12 +@dataclass(slots=True)
    13 +class SimulatorBalances:
    14 +    free_quote: float
    15 +    free_base: float
    16 +
    17 +
    18 +class SimulatedExchange:
    19 +    def __init__(self, settings: Settings, metrics: MetricsTracker) -> N
        one:
    20 +        self.settings = settings
    21 +        self.metrics = metrics
    22 +        self.balances = SimulatorBalances(
    23 +            free_quote=settings.app.initial_cash,
    24 +            free_base=0.0,
    25 +        )
    26 +        self.open_orders: dict[str, ManagedOrder] = {}
    27 +
    28 +    def place_order(self, order: OrderRequest) -> ManagedOrder:
    29 +        managed = ManagedOrder(
    30 +            symbol=order.symbol,
    31 +            side=order.side,
    32 +            price=order.price,
    33 +            quantity=order.quantity,
    34 +            client_order_id=order.client_order_id,
    35 +        )
    36 +        self.open_orders[managed.client_order_id] = managed
    37 +        self.metrics.record_order_submission()
    38 +        logger.info("模拟下单: {}", managed)
    39 +        return managed
    40 +
    41 +    def cancel_order(self, client_order_id: str) -> None:
    42 +        if client_order_id in self.open_orders:
    43 +            logger.info("模拟撤单: {}", client_order_id)
    44 +            self.open_orders.pop(client_order_id, None)
    45 +
    46 +    def process_snapshot(self, snapshot: MarketSnapshot) -> list[FillEve
        nt]:
    47 +        fills: list[FillEvent] = []
    48 +        for client_order_id, order in list(self.open_orders.items()):
    49 +            should_fill = False
    50 +            if order.side == "BUY" and order.price >= snapshot.best_ask:
    51 +                should_fill = True
    52 +            if order.side == "SELL" and order.price <= snapshot.best_bid
        :
    53 +                should_fill = True
    54 +            if not should_fill:
    55 +                continue
    56 +
    57 +            fill = FillEvent(
    58 +                symbol=order.symbol,
    59 +                side=order.side,
    60 +                price=order.price,
    61 +                quantity=order.quantity,
    62 +                liquidity="maker",
    63 +                fee_bps=self.settings.fees.maker_fee_bps,
    64 +                rebate_bps=self.settings.fees.rebate_bps,
    65 +                order_id=order.client_order_id,
    66 +            )
    67 +            self._apply_fill(fill)
    68 +            self.metrics.record_fill(fill)
    69 +            fills.append(fill)
    70 +            self.open_orders.pop(client_order_id, None)
    71 +        return fills
    72 +
    73 +    def _apply_fill(self, fill: FillEvent) -> None:
    74 +        if fill.side == "BUY":
    75 +            self.balances.free_quote -= fill.notional
    76 +            self.balances.free_base += fill.quantity
    77 +        else:
    78 +            self.balances.free_quote += fill.notional
    79 +            self.balances.free_base -= fill.quantity

  └ binance_mm_mvp/binance_mm/metrics.py (+97 -0)
     1 +from __future__ import annotations
     2 +
     3 +from collections import deque
     4 +from dataclasses import dataclass
     5 +
     6 +from binance_mm.models import FillEvent
     7 +from binance_mm.utils import bps_to_fraction
     8 +
     9 +
    10 +@dataclass(slots=True)
    11 +class MetricsSummary:
    12 +    turnover: float
    13 +    gross_pnl: float
    14 +    net_pnl: float
    15 +    fees: float
    16 +    rebate_estimate: float
    17 +    inventory_exposure: float
    18 +    maker_ratio: float
    19 +    taker_ratio: float
    20 +    fill_ratio: float
    21 +    total_fills: int
    22 +
    23 +
    24 +class MetricsTracker:
    25 +    def __init__(self) -> None:
    26 +        self.turnover = 0.0
    27 +        self.fees = 0.0
    28 +        self.rebate_estimate = 0.0
    29 +        self.realized_pnl = 0.0
    30 +        self.inventory_qty = 0.0
    31 +        self.inventory_cost = 0.0
    32 +        self.orders_submitted = 0
    33 +        self.fills: list[FillEvent] = []
    34 +        self._equity_curve: deque[float] = deque(maxlen=10_000)
    35 +
    36 +    def record_order_submission(self, count: int = 1) -> None:
    37 +        self.orders_submitted += count
    38 +
    39 +    def record_fill(self, fill: FillEvent) -> None:
    40 +        self.fills.append(fill)
    41 +        self.turnover += fill.notional
    42 +        fee = fill.notional * bps_to_fraction(fill.fee_bps)
    43 +        rebate = fill.notional * bps_to_fraction(fill.rebate_bps)
    44 +        self.fees += fee
    45 +        self.rebate_estimate += rebate
    46 +
    47 +        if fill.side == "BUY":
    48 +            self.inventory_cost += fill.notional
    49 +            self.inventory_qty += fill.quantity
    50 +        else:
    51 +            avg_cost = self.average_cost
    52 +            self.realized_pnl += (fill.price - avg_cost) * fill.quantity
    53 +            self.inventory_cost -= avg_cost * fill.quantity
    54 +            self.inventory_qty -= fill.quantity
    55 +            if self.inventory_qty < 1e-12:
    56 +                self.inventory_qty = 0.0
    57 +                self.inventory_cost = 0.0
    58 +
    59 +    @property
    60 +    def average_cost(self) -> float:
    61 +        if self.inventory_qty <= 0:
    62 +            return 0.0
    63 +        return self.inventory_cost / self.inventory_qty
    64 +
    65 +    def mark_equity(self, mid_price: float) -> float:
    66 +        unrealized = (mid_price - self.average_cost) * self.inventory_qt
        y if self.inventory_qty else 0.0
    67 +        gross = self.realized_pnl + unrealized
    68 +        net = gross - self.fees + self.rebate_estimate
    69 +        self._equity_curve.append(net)
    70 +        return net
    71 +
    72 +    def summary(self, mid_price: float) -> MetricsSummary:
    73 +        gross_pnl = self.realized_pnl + (
    74 +            (mid_price - self.average_cost) * self.inventory_qty if self
        .inventory_qty else 0.0
    75 +        )
    76 +        net_pnl = gross_pnl - self.fees + self.rebate_estimate
    77 +        maker_count = sum(1 for fill in self.fills if fill.liquidity ==
        "maker")
    78 +        total_fills = len(self.fills)
    79 +        maker_ratio = maker_count / total_fills if total_fills else 0.0
    80 +        taker_ratio = 1.0 - maker_ratio if total_fills else 0.0
    81 +        fill_ratio = total_fills / self.orders_submitted if self.orders_
        submitted else 0.0
    82 +        return MetricsSummary(
    83 +            turnover=self.turnover,
    84 +            gross_pnl=gross_pnl,
    85 +            net_pnl=net_pnl,
    86 +            fees=self.fees,
    87 +            rebate_estimate=self.rebate_estimate,
    88 +            inventory_exposure=abs(self.inventory_qty * mid_price),
    89 +            maker_ratio=maker_ratio,
    90 +            taker_ratio=taker_ratio,
    91 +            fill_ratio=fill_ratio,
    92 +            total_fills=total_fills,
    93 +        )
    94 +
    95 +    @property
    96 +    def equity_curve(self) -> list[float]:
    97 +        return list(self._equity_curve)

  └ binance_mm_mvp/binance_mm/models.py (+123 -0)
      1 +from __future__ import annotations
      2 +
      3 +from dataclasses import dataclass, field
      4 +from datetime import datetime, timezone
      5 +from typing import Literal
      6 +
      7 +from pydantic import BaseModel, ConfigDict
      8 +
      9 +
     10 +Side = Literal["BUY", "SELL"]
     11 +Liquidity = Literal["maker", "taker"]
     12 +
     13 +
     14 +def utc_now() -> datetime:
     15 +    return datetime.now(timezone.utc)
     16 +
     17 +
     18 +@dataclass(slots=True)
     19 +class OrderBookLevel:
     20 +    price: float
     21 +    quantity: float
     22 +
     23 +
     24 +@dataclass(slots=True)
     25 +class MarketSnapshot:
     26 +    symbol: str
     27 +    best_bid: float
     28 +    best_ask: float
     29 +    bid_qty: float
     30 +    ask_qty: float
     31 +    last_trade_price: float
     32 +    last_trade_side: Side = "BUY"
     33 +    event_time: datetime = field(default_factory=utc_now)
     34 +
     35 +    @property
     36 +    def mid_price(self) -> float:
     37 +        return (self.best_bid + self.best_ask) / 2.0
     38 +
     39 +    @property
     40 +    def spread_bps(self) -> float:
     41 +        if self.mid_price <= 0:
     42 +            return 0.0
     43 +        return (self.best_ask - self.best_bid) / self.mid_price * 10_00
         0
     44 +
     45 +    @property
     46 +    def imbalance(self) -> float:
     47 +        total = self.bid_qty + self.ask_qty
     48 +        if total <= 0:
     49 +            return 0.0
     50 +        return (self.bid_qty - self.ask_qty) / total
     51 +
     52 +
     53 +@dataclass(slots=True)
     54 +class QuoteDecision:
     55 +    bid_price: float
     56 +    ask_price: float
     57 +    bid_quantity: float
     58 +    ask_quantity: float
     59 +    spread_bps: float
     60 +    reason: str
     61 +
     62 +
     63 +@dataclass(slots=True)
     64 +class OrderRequest:
     65 +    symbol: str
     66 +    side: Side
     67 +    price: float
     68 +    quantity: float
     69 +    client_order_id: str
     70 +    post_only: bool = True
     71 +
     72 +    @property
     73 +    def notional(self) -> float:
     74 +        return self.price * self.quantity
     75 +
     76 +
     77 +@dataclass(slots=True)
     78 +class ManagedOrder:
     79 +    symbol: str
     80 +    side: Side
     81 +    price: float
     82 +    quantity: float
     83 +    client_order_id: str
     84 +    status: str = "NEW"
     85 +    exchange_order_id: int | None = None
     86 +    created_at: datetime = field(default_factory=utc_now)
     87 +    filled_quantity: float = 0.0
     88 +
     89 +    @property
     90 +    def age_seconds(self) -> float:
     91 +        return max((utc_now() - self.created_at).total_seconds(), 0.0)
     92 +
     93 +
     94 +@dataclass(slots=True)
     95 +class FillEvent:
     96 +    symbol: str
     97 +    side: Side
     98 +    price: float
     99 +    quantity: float
    100 +    liquidity: Liquidity
    101 +    fee_bps: float
    102 +    rebate_bps: float
    103 +    event_time: datetime = field(default_factory=utc_now)
    104 +    order_id: str | None = None
    105 +
    106 +    @property
    107 +    def notional(self) -> float:
    108 +        return self.price * self.quantity
    109 +
    110 +
    111 +class BacktestReport(BaseModel):
    112 +    model_config = ConfigDict(extra="ignore")
    113 +
    114 +    total_return: float
    115 +    max_drawdown: float
    116 +    sharpe: float
    117 +    win_rate: float
    118 +    turnover: float
    119 +    fees: float
    120 +    rebate_estimate: float
    121 +    gross_pnl: float
    122 +    net_pnl: float
    123 +    total_trades: int

  └ binance_mm_mvp/binance_mm/risk.py (+75 -0)
     1 +from __future__ import annotations
     2 +
     3 +from dataclasses import dataclass
     4 +
     5 +from binance_mm.config import RiskConfig
     6 +from binance_mm.metrics import MetricsTracker
     7 +from binance_mm.models import MarketSnapshot, OrderRequest
     8 +
     9 +
    10 +@dataclass(slots=True)
    11 +class RiskDecision:
    12 +    allowed: bool
    13 +    reason: str
    14 +
    15 +
    16 +class RiskManager:
    17 +    def __init__(self, config: RiskConfig) -> None:
    18 +        self.config = config
    19 +        self.api_failure_count = 0
    20 +        self.consecutive_losses = 0
    21 +        self.trading_paused = False
    22 +
    23 +    def allow_trading(self, metrics: MetricsTracker, snapshot: MarketSna
        pshot | None, free_usdt: float) -> RiskDecision:
    24 +        if self.trading_paused:
    25 +            return RiskDecision(False, "交易已被风控暂停")
    26 +        if metrics.summary(snapshot.mid_price if snapshot else 0.0).net_
        pnl <= -abs(self.config.max_daily_loss):
    27 +            return RiskDecision(False, "触发单日最大亏损限制")
    28 +        if self.api_failure_count >= self.config.api_failure_circuit_bre
        aker:
    29 +            return RiskDecision(False, "触发 API 熔断")
    30 +        if self.consecutive_losses >= self.config.max_consecutive_losses
        :
    31 +            return RiskDecision(False, "触发连续亏损限制")
    32 +        if free_usdt < self.config.min_free_usdt:
    33 +            return RiskDecision(False, "可用 USDT 余额不足")
    34 +        if snapshot and snapshot.spread_bps >= self.config.abnormal_vola
        tility_bps:
    35 +            return RiskDecision(False, "盘口波动异常，暂停交易")
    36 +        return RiskDecision(True, "ok")
    37 +
    38 +    def validate_order(
    39 +        self,
    40 +        order: OrderRequest,
    41 +        metrics: MetricsTracker,
    42 +        free_usdt: float,
    43 +        best_bid: float,
    44 +        best_ask: float,
    45 +    ) -> RiskDecision:
    46 +        if order.notional > self.config.max_order_notional:
    47 +            return RiskDecision(False, "超过单笔最大名义价值")
    48 +        projected_inventory = metrics.inventory_qty + (order.quantity if
         order.side == "BUY" else -order.quantity)
    49 +        if abs(projected_inventory) > self.config.max_net_position_base:
    50 +            return RiskDecision(False, "超过最大净持仓限制")
    51 +        if order.side == "BUY" and order.notional > free_usdt:
    52 +            return RiskDecision(False, "余额不足，禁止买单")
    53 +        if order.side == "BUY" and order.price >= best_ask:
    54 +            return RiskDecision(False, "买单可能吃单，超过最大滑点容忍")
    55 +        if order.side == "SELL" and order.price <= best_bid:
    56 +            return RiskDecision(False, "卖单可能吃单，超过最大滑点容忍")
    57 +        return RiskDecision(True, "ok")
    58 +
    59 +    def register_api_success(self) -> None:
    60 +        self.api_failure_count = 0
    61 +
    62 +    def register_api_failure(self) -> None:
    63 +        self.api_failure_count += 1
    64 +
    65 +    def register_trade_result(self, pnl: float) -> None:
    66 +        if pnl < 0:
    67 +            self.consecutive_losses += 1
    68 +        else:
    69 +            self.consecutive_losses = 0
    70 +
    71 +    def pause(self) -> None:
    72 +        self.trading_paused = True
    73 +
    74 +    def resume(self) -> None:
    75 +        self.trading_paused = False

  └ binance_mm_mvp/binance_mm/strategy/market_maker.py (+79 -0)
     1 +from __future__ import annotations
     2 +
     3 +from collections import deque
     4 +
     5 +from binance_mm.config import Settings
     6 +from binance_mm.metrics import MetricsTracker
     7 +from binance_mm.models import MarketSnapshot, QuoteDecision
     8 +from binance_mm.utils import bps_to_fraction, clamp
     9 +
    10 +
    11 +class MarketMakerStrategy:
    12 +    def __init__(self, settings: Settings) -> None:
    13 +        self.settings = settings
    14 +        self.mid_prices: deque[float] = deque(maxlen=settings.strategy.v
        olatility_window)
    15 +        self.trade_sides: deque[int] = deque(maxlen=30)
    16 +
    17 +    def on_snapshot(self, snapshot: MarketSnapshot) -> None:
    18 +        self.mid_prices.append(snapshot.mid_price)
    19 +        self.trade_sides.append(1 if snapshot.last_trade_side == "BUY" e
        lse -1)
    20 +
    21 +    def build_quotes(self, snapshot: MarketSnapshot, metrics: MetricsTra
        cker) -> QuoteDecision:
    22 +        self.on_snapshot(snapshot)
    23 +        volatility = self._volatility_bps()
    24 +        imbalance = snapshot.imbalance
    25 +        trade_bias = sum(self.trade_sides) / len(self.trade_sides) if se
        lf.trade_sides else 0.0
    26 +        inventory_gap = metrics.inventory_qty - self.settings.strategy.i
        nventory_target_base
    27 +
    28 +        spread_bps = self.settings.strategy.base_spread_bps
    29 +        spread_bps += volatility * self.settings.strategy.volatility_spr
        ead_multiplier
    30 +        spread_bps += abs(imbalance) * self.settings.strategy.imbalance_
        spread_multiplier
    31 +        spread_bps += abs(trade_bias) * self.settings.strategy.trade_bia
        s_spread_multiplier
    32 +        spread_bps = clamp(
    33 +            spread_bps,
    34 +            self.settings.strategy.min_spread_bps,
    35 +            self.settings.strategy.max_spread_bps,
    36 +        )
    37 +
    38 +        half_spread = snapshot.mid_price * bps_to_fraction(spread_bps /
        2.0)
    39 +        skew = snapshot.mid_price * bps_to_fraction(
    40 +            inventory_gap * self.settings.strategy.inventory_skew_bps_pe
        r_unit
    41 +        )
    42 +
    43 +        bid_price = snapshot.mid_price - half_spread - skew
    44 +        ask_price = snapshot.mid_price + half_spread - skew
    45 +
    46 +        # 自成交保护：报价必须严格位于盘口内侧，不允许交叉。
    47 +        bid_price = min(bid_price, snapshot.best_ask * (1 - bps_to_fract
        ion(1.0)))
    48 +        ask_price = max(ask_price, snapshot.best_bid * (1 + bps_to_fract
        ion(1.0)))
    49 +        if bid_price >= ask_price:
    50 +            bid_price = snapshot.mid_price * (1 - bps_to_fraction(spread
        _bps))
    51 +            ask_price = snapshot.mid_price * (1 + bps_to_fraction(spread
        _bps))
    52 +
    53 +        quantity = max(self.settings.strategy.order_size_usdt / max(snap
        shot.mid_price, 1e-12), 0.0)
    54 +        reason = (
    55 +            f"spread={spread_bps:.2f}bps vol={volatility:.4f}bps "
    56 +            f"imbalance={imbalance:.4f} trade_bias={trade_bias:.4f} inve
        ntory={metrics.inventory_qty:.6f}"
    57 +        )
    58 +        return QuoteDecision(
    59 +            bid_price=bid_price,
    60 +            ask_price=ask_price,
    61 +            bid_quantity=quantity,
    62 +            ask_quantity=quantity,
    63 +            spread_bps=spread_bps,
    64 +            reason=reason,
    65 +        )
    66 +
    67 +    def _volatility_bps(self) -> float:
    68 +        if len(self.mid_prices) < 2:
    69 +            return 0.0
    70 +        returns = []
    71 +        values = list(self.mid_prices)
    72 +        for prev, cur in zip(values, values[1:]):
    73 +            if prev > 0:
    74 +                returns.append((cur - prev) / prev * 10_000)
    75 +        if not returns:
    76 +            return 0.0
    77 +        mean = sum(returns) / len(returns)
    78 +        variance = sum((r - mean) ** 2 for r in returns) / len(returns)
    79 +        return variance ** 0.5 / 10_000

  └ binance_mm_mvp/binance_mm/utils.py (+48 -0)
     1 +from __future__ import annotations
     2 +
     3 +import math
     4 +import os
     5 +from decimal import Decimal, ROUND_DOWN
     6 +
     7 +
     8 +def getenv_str(name: str, default: str = "") -> str:
     9 +    return os.getenv(name, default).strip()
    10 +
    11 +
    12 +def env_bool(name: str, default: bool = False) -> bool:
    13 +    value = os.getenv(name)
    14 +    if value is None:
    15 +        return default
    16 +    return value.strip().lower() in {"1", "true", "yes", "on"}
    17 +
    18 +
    19 +def clamp(value: float, low: float, high: float) -> float:
    20 +    return max(low, min(high, value))
    21 +
    22 +
    23 +def bps_to_fraction(value_bps: float) -> float:
    24 +    return value_bps / 10_000.0
    25 +
    26 +
    27 +def round_step(value: float, step: float) -> float:
    28 +    if step <= 0:
    29 +        return value
    30 +    d_value = Decimal(str(value))
    31 +    d_step = Decimal(str(step))
    32 +    return float((d_value / d_step).quantize(Decimal("1"), rounding=ROUN
        D_DOWN) * d_step)
    33 +
    34 +
    35 +def round_tick(price: float, tick_size: float) -> float:
    36 +    return round_step(price, tick_size)
    37 +
    38 +
    39 +def safe_stdev(values: list[float]) -> float:
    40 +    if len(values) < 2:
    41 +        return 0.0
    42 +    mean = sum(values) / len(values)
    43 +    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    44 +    return math.sqrt(max(variance, 0.0))
    45 +
    46 +
    47 +def generate_client_order_id(prefix: str, side: str, sequence: int) -> s
        tr:
    48 +    return f"{prefix}-{side.lower()}-{sequence:06d}"

  └ binance_mm_mvp/config.yaml (+49 -0)
     1 +app:
     2 +  name: "binance-mm-mvp"
     3 +  mode: "paper"
     4 +  symbol: "BTCUSDT"
     5 +  quote_asset: "USDT"
     6 +  base_asset: "BTC"
     7 +  kline_interval: "1m"
     8 +  initial_cash: 1000.0
     9 +  testnet: true
    10 +  enable_live_trading: false
    11 +  order_refresh_seconds: 8
    12 +  stale_data_seconds: 5
    13 +  loop_interval_seconds: 1
    14 +
    15 +strategy:
    16 +  base_spread_bps: 6.0
    17 +  min_spread_bps: 4.0
    18 +  max_spread_bps: 25.0
    19 +  order_size_usdt: 50.0
    20 +  max_total_orders: 2
    21 +  max_order_age_seconds: 12
    22 +  inventory_target_base: 0.0
    23 +  inventory_skew_bps_per_unit: 12.0
    24 +  volatility_window: 60
    25 +  volatility_spread_multiplier: 1800.0
    26 +  imbalance_spread_multiplier: 8.0
    27 +  trade_bias_spread_multiplier: 6.0
    28 +  requote_threshold_bps: 3.0
    29 +
    30 +risk:
    31 +  max_daily_loss: 50.0
    32 +  max_order_notional: 100.0
    33 +  max_net_position_base: 0.01
    34 +  max_consecutive_losses: 4
    35 +  max_slippage_bps: 8.0
    36 +  api_failure_circuit_breaker: 5
    37 +  cancel_retry_count: 3
    38 +  abnormal_volatility_bps: 40.0
    39 +  min_free_usdt: 50.0
    40 +
    41 +fees:
    42 +  maker_fee_bps: 1.0
    43 +  taker_fee_bps: 3.5
    44 +  rebate_bps: 0.2
    45 +
    46 +backtest:
    47 +  data_path: "binance_mm/data/sample_klines.csv"
    48 +  assume_fill_on_touch: true
    49 +  random_seed: 7

  └ binance_mm_mvp/main.py (+38 -0)
     1 +from __future__ import annotations
     2 +
     3 +import argparse
     4 +import asyncio
     5 +
     6 +from loguru import logger
     7 +
     8 +from binance_mm.backtest.engine import BacktestEngine
     9 +from binance_mm.config import load_settings
    10 +from binance_mm.engine.live_trader import LiveTrader
    11 +
    12 +
    13 +def parse_args() -> argparse.Namespace:
    14 +    parser = argparse.ArgumentParser(description="Binance quasi market m
        aking strategy MVP")
    15 +    parser.add_argument("--mode", choices=["backtest", "paper", "live"],
         default=None)
    16 +    parser.add_argument("--config", default="config.yaml")
    17 +    parser.add_argument("--env-file", default=".env")
    18 +    return parser.parse_args()
    19 +
    20 +
    21 +async def async_main() -> None:
    22 +    args = parse_args()
    23 +    settings = load_settings(config_path=args.config, env_path=args.env_
        file)
    24 +    mode = args.mode or settings.app.mode
    25 +
    26 +    logger.info("启动模式: {}", mode)
    27 +    if mode == "backtest":
    28 +        engine = BacktestEngine(settings)
    29 +        report = engine.run()
    30 +        logger.info("回测结果: {}", report.model_dump())
    31 +        return
    32 +
    33 +    trader = LiveTrader(settings=settings, mode=mode)
    34 +    await trader.run()
    35 +
    36 +
    37 +if __name__ == "__main__":
    38 +    asyncio.run(async_main())

  └ binance_mm_mvp/requirements.txt (+10 -0)
     1 +python-binance==1.0.19
     2 +websockets==12.0
     3 +pandas==2.2.3
     4 +numpy==2.2.3
     5 +pydantic==2.10.6
     6 +python-dotenv==1.0.1
     7 +loguru==0.7.3
     8 +PyYAML==6.0.2
     9 +pytest==8.3.5
    10 +pytest-asyncio==0.25.3

  └ binance_mm_mvp/tests/test_metrics.py (+18 -0)
     1 +from binance_mm.metrics import MetricsTracker
     2 +from binance_mm.models import FillEvent
     3 +
     4 +
     5 +def test_metrics_summary_contains_turnover_and_inventory() -> None:
     6 +    tracker = MetricsTracker()
     7 +    tracker.record_order_submission(2)
     8 +    tracker.record_fill(
     9 +        FillEvent(symbol="BTCUSDT", side="BUY", price=100.0, quantity=1.
        0, liquidity="maker", fee_bps=1.0, rebate_bps=0.2)
    10 +    )
    11 +    tracker.record_fill(
    12 +        FillEvent(symbol="BTCUSDT", side="SELL", price=101.0, quantity=1
        .0, liquidity="maker", fee_bps=1.0, rebate_bps=0.2)
    13 +    )
    14 +    summary = tracker.summary(101.0)
    15 +    assert summary.turnover == 201.0
    16 +    assert summary.total_fills == 2
    17 +    assert summary.inventory_exposure == 0.0
    18 +    assert summary.fill_ratio == 1.0

  └ binance_mm_mvp/tests/test_risk.py (+27 -0)
     1 +from binance_mm.config import RiskConfig
     2 +from binance_mm.metrics import MetricsTracker
     3 +from binance_mm.models import MarketSnapshot, OrderRequest
     4 +from binance_mm.risk import RiskManager
     5 +
     6 +
     7 +def test_risk_rejects_crossing_buy_order() -> None:
     8 +    risk = RiskManager(RiskConfig())
     9 +    metrics = MetricsTracker()
    10 +    order = OrderRequest(symbol="BTCUSDT", side="BUY", price=101.0, quan
        tity=0.1, client_order_id="x")
    11 +    decision = risk.validate_order(order, metrics, free_usdt=1000.0, bes
        t_bid=99.0, best_ask=100.0)
    12 +    assert not decision.allowed
    13 +
    14 +
    15 +def test_risk_allows_normal_trading() -> None:
    16 +    risk = RiskManager(RiskConfig())
    17 +    metrics = MetricsTracker()
    18 +    snapshot = MarketSnapshot(
    19 +        symbol="BTCUSDT",
    20 +        best_bid=100.0,
    21 +        best_ask=100.05,
    22 +        bid_qty=1.0,
    23 +        ask_qty=1.0,
    24 +        last_trade_price=100.02,
    25 +    )
    26 +    decision = risk.allow_trading(metrics, snapshot, free_usdt=500.0)
    27 +    assert decision.allowed

─ Worked for 5m 06s ────────────────────────────────────────────────────────────

• 核心文件已经落下，接下来做两件事：补齐包初始化文件，并修正一轮明显的实现细节后
  跑本地测试。

• Edited 5 files (+10 -0)
  └ binance_mm_mvp/binance_mm/backtest/__init__.py (+1 -0)
    1 +__all__ = ["engine"]

  └ binance_mm_mvp/binance_mm/clients/__init__.py (+1 -0)
    1 +__all__ = ["binance_client"]

  └ binance_mm_mvp/binance_mm/engine/__init__.py (+1 -0)
    1 +__all__ = ["live_trader", "simulator"]

  └ binance_mm_mvp/binance_mm/risk.py (+6 -0)
     7  from binance_mm.models import MarketSnapshot, OrderRequest
     8 +from binance_mm.utils import bps_to_fraction
     9
       ⋮
    53              return RiskDecision(False, "余额不足，禁止买单")
    54 +        allowed_slippage = bps_to_fraction(self.config.max_slippage_bps)
    55          if order.side == "BUY" and order.price >= best_ask:
       ⋮
    58              return RiskDecision(False, "卖单可能吃单，超过最大滑点容忍")
    59 +        if order.side == "BUY" and best_bid > 0 and (best_bid - order.pr
        ice) / best_bid > allowed_slippage:
    60 +            return RiskDecision(False, "买单偏离买一过大")
    61 +        if order.side == "SELL" and best_ask > 0 and (order.price - best
        _ask) / best_ask > allowed_slippage:
    62 +            return RiskDecision(False, "卖单偏离卖一过大")
    63          return RiskDecision(True, "ok")

  └ binance_mm_mvp/binance_mm/strategy/__init__.py (+1 -0)
    1 +__all__ = ["market_maker"]

• Ran python3 -m pytest -q
  └ /Library/Frameworks/Python.framework/Versions/3.11/bin/python3: No module
    named pytest

• Ran python3 main.py --mode backtest
  └ Traceback (most recent call last):
      File "/Users/daniel/binance_mm_mvp/main.py", line 6, in <module>
        from loguru import logger
    ModuleNotFoundError: No module named 'loguru'

────────────────────────────────────────────────────────────────────────────────

• 本地环境还没装依赖，pytest 和 main.py 直接运行都因为缺少 pytest/loguru 失败。
  我先做不依赖第三方包的语法编译检查，确认项目源码本身没有语法问题。

• Ran python3 -m compileall main.py binance_mm tests
  └ Compiling 'main.py'...
    Listing 'binance_mm'...
    … +21 lines
    Compiling 'tests/test_metrics.py'...
    Compiling 'tests/test_risk.py'...

• Explored
  └ Read live_trader.py
    List binance_mm_mvp

────────────────────────────────────────────────────────────────────────────────

• 我又过了一遍执行路径，发现两个需要收口的地方：行情到来时策略被重复喂了两次，以
  及回测里未成交挂单可能累积过多。现在把这两个实现问题修掉。

• Edited 2 files (+21 -8)
  └ binance_mm_mvp/binance_mm/backtest/engine.py (+6 -0)
     50                  quote = self.strategy.build_quotes(snapshot, self.metri
         cs)
     51 +                self._trim_open_orders()
     52                  buy_order = OrderRequest(
        ⋮
    141
    142 +    def _trim_open_orders(self) -> None:
    143 +        while len(self.open_orders) >= self.settings.strategy.max_total
         _orders:
    144 +            oldest_order_id = next(iter(self.open_orders))
    145 +            self.open_orders.pop(oldest_order_id, None)
    146 +
    147      def _max_drawdown(self, values: list[float]) -> float:

  └ binance_mm_mvp/binance_mm/engine/live_trader.py (+15 -8)
    126
    127 -        await self._replace_quotes(snapshot, free_usdt)
    127 +        await self._replace_quotes(snapshot, free_usdt, quote.bid_price
         , quote.ask_price, quote.bid_quantity, quote.ask_quantity)
    128          summary = self.metrics.summary(snapshot.mid_price)
        ⋮
    130
    131 -    async def _replace_quotes(self, snapshot: MarketSnapshot, free_usdt
         : float) -> None:
    132 -        quote = self.strategy.build_quotes(snapshot, self.metrics)
    131 +    async def _replace_quotes(
    132 +        self,
    133 +        snapshot: MarketSnapshot,
    134 +        free_usdt: float,
    135 +        bid_price: float,
    136 +        ask_price: float,
    137 +        bid_quantity: float,
    138 +        ask_quantity: float,
    139 +    ) -> None:
    140          await self._cancel_stale(force_all=True)
        ⋮
    145                  side="BUY",
    139 -                price=quote.bid_price,
    140 -                quantity=quote.bid_quantity,
    146 +                price=bid_price,
    147 +                quantity=bid_quantity,
    148                  client_order_id=self._next_client_order_id("BUY"),
        ⋮
    152                  side="SELL",
    146 -                price=quote.ask_price,
    147 -                quantity=quote.ask_quantity,
    153 +                price=ask_price,
    154 +                quantity=ask_quantity,
    155                  client_order_id=self._next_client_order_id("SELL"),
        ⋮
    182              self.open_orders[managed.client_order_id] = managed
    176 -        self.last_quote = (quote.bid_price, quote.ask_price)
    183 +        self.last_quote = (bid_price, ask_price)
    184

• Ran python3 -m compileall main.py binance_mm tests
  └ Listing 'binance_mm'...
    Listing 'binance_mm/backtest'...
    … +5 lines
    Listing 'binance_mm/strategy'...
    Listing 'tests'...

• Explored
  └ Search */__pycache__/* in binance_mm_mvp

• Updated Plan
  └ 项目源码、配置、README 和测试样例已经生成，完成了语法编译检查。由于当前环境
    未安装第三方依赖，pytest 与运行入口未做依赖级实测。
    ✔ 设计项目结构与配置模型，明确模块边界和默认参数
    ✔ 实现 Binance 客户端、WebSocket、策略、风控、指标、回测与运行入口
    ✔ 补充 README、示例配置、requirements 和单元测试
    ✔ 运行基础测试与静态启动检查，整理最终输出

────────────────────────────────────────────────────────────────────────────────

• 项目已生成在 /Users/daniel/binance_mm_mvp。完整源码、配置、README、示例数据和
  测试样例都已落盘。

  结构树

  binance_mm_mvp/
  ├── .env.example
  ├── README.md
  ├── config.yaml
  ├── main.py
  ├── requirements.txt
  ├── binance_mm/
  │   ├── __init__.py
  │   ├── config.py
  │   ├── metrics.py
  │   ├── models.py
  │   ├── risk.py
  │   ├── utils.py
  │   ├── clients/
  │   │   ├── __init__.py
  │   │   └── binance_client.py
  │   ├── strategy/
  │   │   ├── __init__.py
  │   │   └── market_maker.py
  │   ├── engine/
  │   │   ├── __init__.py
  │   │   ├── live_trader.py
  │   │   └── simulator.py
  │   ├── backtest/
  │   │   ├── __init__.py
  │   │   └── engine.py
  │   └── data/
  │       └── sample_klines.csv
  └── tests/
      ├── test_metrics.py
      └── test_risk.py

  代码文件
  完整代码已写入这些文件，你可以直接打开：
  README.md
  config.yaml
  main.py
  requirements.txt
  config.py
  metrics.py
  models.py
  risk.py
  binance_client.py
  market_maker.py
  live_trader.py
  simulator.py
  engine.py
  test_metrics.py
  test_risk.py

  安装命令

  cd /Users/daniel/binance_mm_mvp
  python3.11 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env

  启动命令

  python main.py --mode backtest
  python main.py --mode paper
  python main.py --mode live

  模拟盘/实盘切换

  - 模拟盘：python main.py --mode paper，并保持 .env 中
    ENABLE_LIVE_TRADING=false
  - 实盘：.env 里改成 ENABLE_LIVE_TRADING=true，同时 config.yaml 中
    app.enable_live_trading: true，再执行 python main.py --mode live
  - 项目做了双开关保护，默认不会真实下单

  API Key 配置
  在 .env.example 同格式创建 .env：

  BINANCE_API_KEY=your_api_key
  BINANCE_API_SECRET=your_api_secret
  BASE_URL=https://api.binance.com
  TESTNET=true
  ENABLE_LIVE_TRADING=false

  风险说明

  - 不承诺收益，成交量仅作统计指标，不能用于刷量或制造虚假交易量。
  - 策略默认只做双边限价挂单，禁止无限追单、Martingale、无限加仓。
  - 已实现日亏损限制、单笔金额限制、最大净仓位、连续亏损限制、滑点保护、API 熔
    断、异常波动暂停、余额不足禁下单、WebSocket 重连、撤单重试、自成交保护。
  - 简化回测不能替代真实撮合环境。

  后续增强方向

  - 接入本地增量深度簿与队列位置估计。
  - 增加部分成交、订单排队、真实 maker 成交概率建模。
  - 加入趋势过滤、时段过滤、库存 alpha 和多档报价。
  - 将成交、PnL、手续费、返佣持久化到 SQLite/Parquet。
  - 加入 Prometheus/Grafana 监控和告警。
  - 按 Binance VIP 等级动态更新手续费与返佣。

  验证情况：python3 -m compileall main.py binance_mm tests 已通过。当前机器未安
  装 loguru、pytest 等依赖，所以 pytest 和运行入口没有在本机完成依赖级实测。

 
› Find and fix a bug in @filename
 
  gpt-5.4 medium · 88% left · ~
