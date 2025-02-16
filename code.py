# ここにコードを書いてね :-)
import board
import digitalio
import time

# SNESコントローラーのピン設定
latch = digitalio.DigitalInOut(board.GP2)  # ラッチピン
clock = digitalio.DigitalInOut(board.GP3)  # クロックピン
data = digitalio.DigitalInOut(board.GP4)   # データピン

# ピンの方向設定
latch.direction = digitalio.Direction.OUTPUT
clock.direction = digitalio.Direction.OUTPUT
data.direction = digitalio.Direction.INPUT

# プルアップ抵抗を有効化
data.pull = digitalio.Pull.UP

# ボタンの名前を定義
button_names = [
    'B', 'Y', 'Select', 'Start',
    'Up', 'Down', 'Left', 'Right',
    'A', 'X', 'L', 'R'
]

def read_snes_controller():
    # ラッチパルスを送信（12μs）
    latch.value = True
    time.sleep(0.000012)
    latch.value = False

    button_states = []

    # 12ビット分のデータを読み取り
    for _ in range(12):
        button_states.append(not data.value)  # データはアクティブLOWなので反転

        # クロックパルスを送信（6μs）
        clock.value = True
        time.sleep(0.000006)
        clock.value = False
        time.sleep(0.000006)

    return button_states

while True:
    # コントローラーの状態を読み取り
    states = read_snes_controller()

    # 押されているボタンを表示
    pressed_buttons = [name for state, name in zip(states, button_names) if state]
    if pressed_buttons:
        print("Pressed buttons:", ", ".join(pressed_buttons))

    # 適度な待機時間
    time.sleep(0.1)
