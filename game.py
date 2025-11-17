import random
import copy
import os
import sys
import yaml
import time
import csv
from datetime import datetime

# 尝试导入 colorama 以实现彩色输出
try:
    import colorama
    colorama.init(autoreset=True)
    USE_COLOR = True
except ImportError:
    USE_COLOR = False

CONFIG_FILE_NAME = 'config.yaml'
DEFAULT_SIZE = 4
RECORD_FILE_NAME = 'record.csv'

class Game2048:
    """
    2048 游戏的核心逻辑类。
    
    属性:
        size (int): 游戏板的大小 (默认为 4x4).
        board (list[list[int]]): 存储游戏板状态的二维列表。
        score (int): 当前游戏分数。
        win_value (int): 游戏胜利的目标分数 (默认为 2048).
        game_won (bool): 标记游戏是否已胜利。
        use_color (bool): 是否使用彩色终端输出。
    """

    # 为不同的数字块定义颜色
    TILE_COLORS = {
        0: colorama.Fore.RESET if USE_COLOR else "",
        2: colorama.Fore.YELLOW if USE_COLOR else "",
        4: colorama.Fore.GREEN if USE_COLOR else "",
        8: colorama.Fore.CYAN if USE_COLOR else "",
        16: colorama.Fore.BLUE if USE_COLOR else "",
        32: colorama.Fore.MAGENTA if USE_COLOR else "",
        64: colorama.Fore.RED if USE_COLOR else "",
        128: colorama.Fore.LIGHTYELLOW_EX if USE_COLOR else "",
        256: colorama.Fore.LIGHTGREEN_EX if USE_COLOR else "",
        512: colorama.Fore.LIGHTCYAN_EX if USE_COLOR else "",
        1024: colorama.Fore.LIGHTBLUE_EX if USE_COLOR else "",
        2048: colorama.Fore.LIGHTMAGENTA_EX if USE_COLOR else "",
        4096: colorama.Fore.LIGHTRED_EX if USE_COLOR else "",
    }
    
    RESET_COLOR = colorama.Fore.RESET if USE_COLOR else ""

    def __init__(self, size=4):
        """初始化游戏板，分数，并添加两个初始图块。"""
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.win_value = 2048
        self.game_won = False
        self.use_color = USE_COLOR

        # 游戏开始时添加两个新图块
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """在随机的空白位置添加一个新图块 (90% 为 2, 10% 为 4)。"""
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))

        if not empty_cells:
            return  # 没有空位了

        (r, c) = random.choice(empty_cells)
        # 90% 几率是 2, 10% 几率是 4
        self.board[r][c] = 4 if random.random() < 0.1 else 2

    def print_board(self):
        """
        清空屏幕并打印当前的游戏板和分数。
        使用 ANSI 颜色代码（如果 colorama 可用）。
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- 2048 游戏 ---")
        print(f"分数: {self.score}")
        print("-------------------")
        
        if self.game_won:
            win_color = self.TILE_COLORS.get(self.win_value, self.RESET_COLOR)
            print(f"{win_color}🎉 你达到了 {self.win_value}! 恭喜! (可以继续玩){self.RESET_COLOR}")

        print("")
        for r in range(self.size):
            for c in range(self.size):
                val = self.board[r][c]
                color = self.TILE_COLORS.get(val, self.RESET_COLOR)
                # 使用 :^6 来居中显示，并保证宽度一致
                print(f"|{color}{val:^6}{self.RESET_COLOR}", end="")
            print("|\n")  # 每行末尾换行
        
        print("-------------------")
        print("使用 W(上) A(左) S(下) D(右) 移动, Q 退出。")

    def is_game_over(self):
        """
        检查游戏是否结束。
        结束条件：
        1. 没有空单元格 (0)。
        2. 没有任何相邻的单元格 (水平或垂直) 具有相同的值。
        """
        # 1. 检查是否有空单元格
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return False  # 还有空位，游戏未结束

        # 2. 检查是否有可合并的相邻单元格
        for r in range(self.size):
            for c in range(self.size):
                # 检查右侧
                if c + 1 < self.size and self.board[r][c] == self.board[r][c+1]:
                    return False
                # 检查下方
                if r + 1 < self.size and self.board[r][c] == self.board[r+1][c]:
                    return False
        
        # 如果以上条件都不满足，则游戏结束
        return True

    def move(self, direction):
        """
        处理玩家的移动 (w, a, s, d)。
        返回:
            bool: 如果移动有效 (棋盘发生变化)，则返回 True，否则返回 False。
        """
        # 深度复制原始棋盘，用于检查移动是否有效
        original_board = copy.deepcopy(self.board)
        
        # 我们将所有操作（上、下、右）都转换为“向左”操作
        # 这样只需要实现 'move_left' 的核心逻辑
        
        if direction == 'w':  # 上
            temp_board = self._transpose(self.board)
            temp_board = self._move_left(temp_board)
            self.board = self._transpose(temp_board)
        elif direction == 's':  # 下
            temp_board = self._transpose(self.board)
            temp_board = self._reverse(temp_board)
            temp_board = self._move_left(temp_board)
            temp_board = self._reverse(temp_board)
            self.board = self._transpose(temp_board)
        elif direction == 'a':  # 左
            self.board = self._move_left(self.board)
        elif direction == 'd':  # 右
            temp_board = self._reverse(self.board)
            temp_board = self._move_left(temp_board)
            self.board = self._reverse(temp_board)
        else:
            return False  # 无效方向

        # 检查棋盘是否发生变化
        if self.board == original_board:
            return False  # 移动无效

        # 移动有效，添加一个新图块
        self.add_new_tile()
        return True

    # --- 移动的辅助方法 ---

    def _move_left(self, board):
        """
        核心逻辑：将所有行向左压缩和合并。
        返回一个新的棋盘 (list[list[int]])。
        """
        new_board = []
        for row in board:
            # 1. 压缩：将所有非零数字移到左侧
            compressed_row = [i for i in row if i != 0]
            
            # 2. 合并：合并相邻的相同数字
            merged_row = []
            i = 0
            while i < len(compressed_row):
                if i + 1 < len(compressed_row) and compressed_row[i] == compressed_row[i+1]:
                    # 发现合并
                    merged_val = compressed_row[i] * 2
                    merged_row.append(merged_val)
                    
                    # 更新分数
                    self.score += merged_val
                    
                    # 检查是否胜利
                    if not self.game_won and merged_val == self.win_value:
                        self.game_won = True
                        
                    i += 2  # 跳过下一个已合并的图块
                else:
                    merged_row.append(compressed_row[i])
                    i += 1
            
            # 3. 再次压缩：用 0 填充右侧的空位
            merged_row += [0] * (self.size - len(merged_row))
            new_board.append(merged_row)
            
        return new_board

    def _transpose(self, board):
        """矩阵转置（行变列，列变行）。"""
        return [list(row) for row in zip(*board)]

    def _reverse(self, board):
        """反转棋盘中的每一行。"""
        return [row[::-1] for row in board]


def get_board_size_from_config():
    """
    从 config.yaml 读取、验证并返回棋盘大小。
    如果文件/配置无效，则返回默认值 4。
    """
    try:
        with open(CONFIG_FILE_NAME, 'r') as f:
            config = yaml.safe_load(f)
            
            # 检查 config 是否为空或不是字典
            if not isinstance(config, dict):
                print(f"提示: '{CONFIG_FILE_NAME}' 为空或格式无效，使用默认大小 {DEFAULT_SIZE}x{DEFAULT_SIZE}。")
                return DEFAULT_SIZE

            board_size_value = config.get('board_size')

            # 检查 'board_size' 是否为空 (None) 或未设置 ('' 也视为空)
            if board_size_value is None or board_size_value == "":
                print(f"提示: 'board_size' 在 '{CONFIG_FILE_NAME}' 中为空或未设置。")
                print(f"使用默认大小 {DEFAULT_SIZE}x{DEFAULT_SIZE}。")
                return DEFAULT_SIZE
            
            # 尝试转换为整数并验证范围
            try:
                size_input = int(board_size_value)
                if 3 <= size_input <= 8:
                    print(f"已从 '{CONFIG_FILE_NAME}' 加载棋盘大小: {size_input}x{size_input}。")
                    return size_input
                else:
                    print(f"警告: '{CONFIG_FILE_NAME}' 中的 'board_size' ({size_input}) 超出 3-8 范围。")
                    print(f"使用默认大小 {DEFAULT_SIZE}x{DEFAULT_SIZE}。")
                    return DEFAULT_SIZE
            except (ValueError, TypeError):
                print(f"警告: '{CONFIG_FILE_NAME}' 中的 'board_size' ('{board_size_value}') 不是有效整数。")
                print(f"使用默认大小 {DEFAULT_SIZE}x{DEFAULT_SIZE}。")
                return DEFAULT_SIZE

    except FileNotFoundError:
        print(f"提示: 未找到 '{CONFIG_FILE_NAME}'。")
        print(f"使用默认大小 {DEFAULT_SIZE}x{DEFAULT_SIZE}。")
        # 提示：可以自动创建默认文件，但这里保持简单
        return DEFAULT_SIZE
    except yaml.YAMLError as e:
        print(f"警告: 解析 '{CONFIG_FILE_NAME}' 出错: {e}")
        print(f"使用默认大小 {DEFAULT_SIZE}x{DEFAULT_SIZE}。")
        return DEFAULT_SIZE


def log_game_result(score, game_won):
    """
    将游戏结果记录到 record.csv 文件。
    格式: [时间], [分数], [+]
    """
    try:
        # 1. 获取当前时间并格式化
        end_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        # 2. 确定胜利状态
        win_status = "+" if game_won else ""
        
        # 3. 准备数据行
        row_data = [end_time, score, win_status]
        
        # 4. 写入文件
        # 'a' (append) 模式会自动创建不存在的文件，并在文件末尾追加
        # newline='' 是写入csv文件时的标准做法，防止空行
        with open(RECORD_FILE_NAME, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row_data)
            
    except IOError as e:
        # 在主游戏循环之外打印，避免立即被清屏
        print(f"\n警告: 无法写入记录到 '{RECORD_FILE_NAME}'. 错误: {e}")
        print("游戏分数未被记录。")
    except Exception as e:
        print(f"\n警告: 记录游戏结果时发生未知错误: {e}")


def main():
    """游戏主循环。"""
    
    # --- 1. 从 config.yaml 获取棋盘大小 ---
    size = get_board_size_from_config()
    
    # --- 2. 检查 colorama ---
    if not USE_COLOR:
        print("提示: 模块 'colorama' 未找到。")
        print("游戏将以黑白模式运行。")
        print("可以尝试运行 'pip install colorama' 来安装彩色支持。")
    
    # --- 3. 统一暂停 ---
    print("\n--- 游戏将在 3 秒后开始 ---")
    time.sleep(3)
    
    # --- 4. 初始化游戏 ---
    game = Game2048(size=size)

    while True:
        # 1. 打印游戏板
        game.print_board()

        # 2. 检查游戏结束条件
        if game.is_game_over():
            print("GAME OVER! 无法再移动。")
            print(f"你的最终分数是: {game.score}")
            
            # --- 新增：记录游戏结果 ---
            log_game_result(game.score, game.game_won)
            # -------------------------
            
            break

        # 3. 获取用户输入
        move = input("输入移动 (w/a/s/d) 或 q 退出: ").lower().strip()

        # 4. 处理输入
        if move == 'q':
            print("感谢游玩，再见！")
            
            # --- 新增：记录游戏结果 (主动退出也记录) ---
            log_game_result(game.score, game.game_won)
            # -------------------------
            
            break
        
        if move not in ['w', 'a', 's', 'd']:
            print("无效输入！请只使用 w, a, s, d 或 q。")
            input("按回车键继续...") # 暂停以显示错误信息
            continue

        # 5. 执行移动
        if not game.move(move):
            print("无效移动！(棋盘未发生变化)")
            # 同样暂停，让用户看到提示
            input("按回车键继续...")


if __name__ == "__main__":
    main()