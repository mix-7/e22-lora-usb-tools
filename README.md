# E22 LoRa USB Tools 📡

> Python tools for Ebyte **E22-900T22U** (USB version) LoRa modules.  
> Text chat, file transfer, and configuration — **no GPIO required**.

[🇷🇺 Русская версия](#-русская-версия) • [Issues](../../issues) • [Releases](../../releases)

![Python](https://shields.io)
![License](https://shields.io)
![Status](https://shields.io)

---

## ✨ Features

- 💬 Half-duplex text chat between two modules
- 📦 File transfer with ACK protocol
- ⚙️ Read/write module parameters (channel, power, speed) via USB
- 🔁 Software mode switching (no button press after first setup)
- 🐍 Pure Python 3, cross-platform (Windows/Linux/macOS)

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Find your port
- **Linux:** `ls /dev/ttyUSB*` → `/dev/ttyUSB0`
- **Windows:** Device Manager → Ports → `COM3`
- **macOS:** `ls /dev/cu.usbserial*`

### 3. First-time setup (ONE TIME per module)
```bash
# Edit src/lora_app.py: set FIRST_RUN = True
python3 src/lora_app.py /dev/ttyUSB0
# Follow on-screen instructions (press button once)
# Then set FIRST_RUN = False and save
```

### 4. Run chat
```bash
python3 src/lora_app.py /dev/ttyUSB0
# Commands: send <message> | quit
```

### 5. Configure module (optional)
```bash
python3 src/config_tool.py /dev/ttyUSB0 read
python3 src/config_tool.py /dev/ttyUSB0 channel 25
python3 src/config_tool.py /dev/ttyUSB0 power 17
```

---

## 📋 Module Parameters Reference

| Parameter | Register | Range | Default |
| :--- | :--- | :--- | :--- |
| Module Address | 0x00-0x01 | 0x0000-0xFFFF | 0x0000 |
| Network ID | 0x02 | 0x00-0xFF | 0x00 |
| Channel | 0x05 | 0-80 (900MHz) | 18 |
| UART Baud | 0x03[7:5] | 1200-115200 | 9600 |
| Air Rate | 0x03[2:0] | 2.4k-62.5k | 2.4k |
| Power | 0x04[7:6] | 22/17/13/10 dBm | 22 dBm |
| Packet Size | 0x04[5:4] | 32/64/128/240 bytes | 240 |

📌 **Frequency formula for E22-900T22U:** `850.125 + channel × 1 MHz`

---

## 🇷🇺 Русская версия

> Инструменты Python для LoRa-модулей **Ebyte E22-900T22U** (USB-версия).  
> Текстовый чат, передача файлов и настройка — **без подключения GPIO**.

### 🚀 Быстрый старт

1. **Установка:** `pip install -r requirements.txt`
2. **Порт:** Linux → `/dev/ttyUSB0`, Windows → `COM3`, macOS → `/dev/cu.usbserial*`
3. **Первая настройка** (1 раз на модуль):
   - В `src/lora_app.py` поставьте `FIRST_RUN = True`
   - Запустите: `python3 src/lora_app.py /dev/ttyUSB0`
   - Нажмите кнопку на модуле >1.5 сек, следуйте инструкциям
   - Верните `FIRST_RUN = False`
4. **Чат:** `python3 src/lora_app.py /dev/ttyUSB0`
5. **Настройка:** `python3 src/config_tool.py /dev/ttyUSB0 read`

### 📋 Команды чата
  
| Команда | Описание |
| :--- | :--- |
| `send <текст>` | Отправить сообщение |
| `quit` | Выход из программы |
| `/cfg` | Показать параметры модуля |

### ⚙️ Настройка параметров

```bash
# Прочитать текущие настройки
python3 src/config_tool.py /dev/ttyUSB0 read
  
# Сменить канал (0-80)
python3 src/config_tool.py /dev/ttyUSB0 channel 25

# Сменить мощность (22/17/13/10 dBm)
python3 src/config_tool.py /dev/ttyUSB0 power 17
```

### 📊 Таблица параметров модуля

| Параметр | Регистр | Диапазон | По умолчанию |
| :--- | :--- | :--- | :--- |
| Адрес модуля | 0x00-0x01 | 0x0000-0xFFFF | 0x0000 |
| Сетевой ID | 0x02 | 0x00-0xFF | 0x00 |
| Канал | 0x05 | 0-80 (900МГц) | 18 |
| UART скорость | 0x03[7:5] | 1200-115200 | 9600 |
| Air скорость | 0x03[2:0] | 2.4k-62.5k | 2.4k |
| Мощность | 0x04[7:6] | 22/17/13/10 dBm | 22 dBm |
| Размер пакета | 0x04[5:4] | 32/64/128/240 байт | 240 |

📌 **Формула частоты для E22-900T22U:** `850.125 + канал × 1 МГц`

---

## 📁 Project Structure

```text
e22-lora-usb-tools/
├── README.md               # This file
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT License
├── requirements.txt        # Python dependencies
├── .gitignore              # Exclude cache, IDE files
│
├── src/                    # Source code
│   ├── e22_usb.py          # Low-level driver
│   ├── lora_app.py         # Interactive chat app
│   └── config_tool.py      # CLI configuration utility
│
├── examples/               # Code snippets
│   ├── basic_chat.py       # Minimal chat example
│   └── read_config.py      # Non-interactive config reader
│
└── docs/                   # Extended documentation
    ├── protocol.md         # E22 command protocol details
    └── troubleshooting.md  # Common issues & solutions
```

---

## 🔧 Requirements

- Python 3.7+
- `pyserial` (install via `pip install pyserial`)
- Ebyte E22-900T22U (USB version) or compatible E22-xxxT22U module

---

## ⚠️ Important Notes

1. **First setup is mandatory:** Run with `FIRST_RUN = True` once to enable software mode switching. After that, no button press is needed.
2. **Both modules must match:** Same `channel`, `air rate`, and compatible `address/netid` for communication.
3. **Half-duplex:** Modules cannot receive while transmitting. The ACK protocol handles this.
4. **USB drivers:** Ensure CH340/CP210x drivers are installed on your system.

---

## 🤝 Contributing

Issues and PRs welcome! Please:
1. Check existing issues first.
2. Describe your setup (OS, Python version, module firmware).
3. Include logs if reporting a bug.

---

## 📜 License

MIT License — see `LICENSE` file.

---

_Made with ❤️ for the LoRa community_
