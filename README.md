# 贪吃蛇

一个使用 Python 标准库编写的桌面贪吃蛇游戏。界面使用 `tkinter`，游戏规则与界面分离，因此无需启动窗口即可完整测试核心逻辑。

## 功能

- 方向键或 `WASD` 控制移动
- 空格键开始或暂停
- `R` 键随时重新开始
- 吃到食物后计分，并随分数提高逐渐加速
- 撞墙或撞到自己时结束游戏
- 蛇占满棋盘时显示胜利状态

## 运行

需要 Python 3.10 或更高版本，并确保 Python 包含 `tkinter`（Windows 和 macOS 的官方 Python 通常已包含）。

```powershell
python -m snake_game
```

也可以安装为命令行程序：

```powershell
python -m pip install -e .
snake-game
```



## 操作

| 按键 | 动作 |
| --- | --- |
| 方向键 / `WASD` | 改变方向 |
| 空格 | 开始 / 暂停 / 继续 |
| `R` | 重新开始 |

