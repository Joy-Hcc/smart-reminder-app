# 智能提醒 App

## 项目结构

```
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── api/       # 路由
│   │   ├── models/    # 数据库模型
│   │   ├── schemas/   # Pydantic 验证
│   │   ├── services/  # 业务逻辑
│   │   └── tasks/     # 调度任务
│   └── requirements.txt
├── frontend/          # Flutter 前端
│   ├── lib/
│   │   ├── config/    # 主题/路由
│   │   ├── models/    # 数据模型
│   │   ├── providers/ # 状态管理
│   │   ├── screens/   # 页面
│   │   ├── widgets/   # 组件
│   │   └── services/  # API调用
│   └── pubspec.yaml
```

## 快速启动

### 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # 编辑配置
python -m uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend
flutter pub get
flutter run
```

## 核心功能

- 设备ID识别用户（零注册）
- 树状分类管理
- 定时/事件触发提醒
- 邮件推送（SendGrid）
- 历史记录追溯

## 技术栈

- 后端：FastAPI + SQLAlchemy + APScheduler
- 前端：Flutter 3.x + Riverpod + Dio
- 天气：和风天气 API
