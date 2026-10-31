#!/usr/bin/env bash
#
# Деплой Telegram-бота на Ubuntu VPS (systemd).
# Запускать из корня проекта: bash deploy/run.sh
#
set -euo pipefail

SERVICE_NAME="crypto-security-bot"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_USER="${SUDO_USER:-$(whoami)}"

echo "Проект: $PROJECT_DIR"
echo "Пользователь сервиса: $RUN_USER"

# --- 1. Токен ---
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
    echo "Создан $PROJECT_DIR/.env — впишите токен от @BotFather и запустите скрипт повторно:"
    echo "  nano $PROJECT_DIR/.env && bash deploy/run.sh"
    exit 1
fi

# --- 2. Системные пакеты (python3-venv нужен для venv) ---
if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Устанавливаю python3-venv..."
    sudo apt-get update -qq
    sudo apt-get install -y -qq python3-venv
fi

# --- 3. Виртуальное окружение + зависимости ---
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "Создаю venv..."
    python3 -m venv "$PROJECT_DIR/venv"
fi
"$PROJECT_DIR/venv/bin/pip" install -q --upgrade pip
"$PROJECT_DIR/venv/bin/pip" install -q -r "$PROJECT_DIR/requirements.txt"

mkdir -p "$PROJECT_DIR/data"

# --- 4. Systemd-юнит (генерируется с фактическими путями) ---
# ВАЖНО: WorkingDirectory=src, т.к. main.py использует плоские импорты (from config import ...)
sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" >/dev/null <<EOF
[Unit]
Description=Crypto Security Bot (Telegram)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${RUN_USER}
WorkingDirectory=${PROJECT_DIR}/src
ExecStart=${PROJECT_DIR}/venv/bin/python main.py
Restart=on-failure
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# --- 5. Запуск и автозагрузка ---
sudo systemctl daemon-reload
sudo systemctl enable --now "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo ""
echo "✅ Готово. Команды управления:"
echo "   systemctl status $SERVICE_NAME      # статус"
echo "   journalctl -u $SERVICE_NAME -f      # живые логи"
echo "   sudo systemctl restart $SERVICE_NAME # перезапуск (например после смены токена)"
echo "   sudo systemctl stop $SERVICE_NAME"
