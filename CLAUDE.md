# Smart Reminder App

## 项目概述

FastAPI + Flutter 智能提醒应用，支持定时/事件触发提醒、邮件推送、树状分类管理。

## 技术栈

- 后端：FastAPI + SQLAlchemy + APScheduler + SQLite
- 前端：Flutter 3.x + Riverpod + Dio + Hive

## 项目结构

```
backend/
├── app/
│   ├── api/          # FastAPI 路由
│   ├── models/       # SQLAlchemy 模型
│   ├── schemas/      # Pydantic 验证
│   ├── services/     # 业务逻辑
│   └── tasks/        # APScheduler 定时任务
├── tests/
└── requirements.txt

frontend/
├── lib/
│   ├── config/       # 主题、路由
│   ├── models/       # 数据模型
│   ├── providers/    # Riverpod 状态管理
│   ├── screens/      # 页面
│   ├── services/     # API、本地存储
│   └── widgets/      # 组件
└── pubspec.yaml
```

## 启动命令

```bash
# 后端
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# 前端
cd frontend
flutter pub get
flutter run
```

---

## Karpathy 编程行为准则

> 源自 Andrej Karpathy 对 LLM 编程常见错误的观察。这些准则偏向谨慎而非速度，简单任务可用自己判断。

### 1. 先想后写（Think Before Coding）

**不要假设，不要隐藏困惑，主动暴露权衡。**

动手之前：
- 明确陈述你的假设。如果不确定，直接问
- 如果有多种理解方式，全部列出来——不要默默选一个
- 如果有更简单的方案，说出来。必要时 push back
- 如果有东西不清楚，停住。指出困惑点，问清楚

### 2. 简单至上（Simplicity First）

**解决问题的代码越少越好。不要写推测性代码。**

- 不添加未要求的功能
- 不为只调用一次的代码建抽象层
- 不加未被要求的"灵活性"或"可配置性"
- 不为不可能发生的场景写 error handling
- 写了200行但50行能搞定 → 重写

自问："senior engineer 会觉得这过度设计吗？"如果会，简化。

### 3. 精准修改（Surgical Changes）

**只动必须动的。只清理自己弄脏的。**

编辑已有代码时：
- 不要"顺便优化"相邻代码、注释或格式
- 不要重构没坏的东西
- 匹配现有风格，即使你更习惯另一种写法
- 发现无关的死代码 → 提一句就行，不要顺手删

代码 diff 检验标准：每一行改动都能追溯到用户的具体需求。

### 4. 目标驱动执行（Goal-Driven Execution）

**定义可验证的成功标准，循环直到达标。**

把任务转化成可验证的目标：
- "加个验证" → "先给非法输入写测试，再让它通过"
- "修这个 bug" → "先写能复现的测试，再让它通过"
- "重构 X" → "确保重构前后测试都绿"

多步骤任务用这种格式：
```
1. [步骤] → 验证: [检查项]
2. [步骤] → 验证: [检查项]
3. [步骤] → 验证: [检查项]
```

好的成功标准让你能独立迭代，差的标准（"把它弄好"）需要反复确认。
