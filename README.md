# Mega Links Checker Bot

A Telegram bot to check MEGA.nz links displays file/folder names, sizes, lists files and folders in with log channel support.


## Deployment Guide

<details>
  <summary><strong>Heroku (One-Click Deploy)</strong></summary>

  1. **Fork this repo**
  2. **Click:**  
      <a href="https://heroku.com/deploy?template=https://github.com/XalFH/Mega-Links-Checker">
        <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" />
      </a>
  3. **Fill required vars:**  
      - `BOT_TOKEN`  
      - `API_ID`  
      - `API_HASH`
      - `LOG_CHANNEL`(optional)
  4. **Deploy and run!**

</details>

<details>
  <summary><strong>VPS / Locally</strong></summary>

  1. **Clone the repository:**
      ```sh
      git clone https://github.com/XalFH/Mega-Links-Checker.git
      cd Mega-Links-Checker
      ```

  2. **Install dependencies:**
      ```sh
      pip install -r requirements.txt
      ```

  3. **Configure bot:**
      - Edit `config.py` with your Telegram API ID, HASH, & BOT TOKEN.

  4. **Run the bot:**
      ```sh
      python3 main.py
      ```

</details>

## Variables 

<details>
  <summary><strong>View Required Variables</strong></summary>

  <br>

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | **Yes** | Your Telegram Bot Token from [@BotFather](https://t.me/BotFather) |
| `API_ID` | **Yes** | Your Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | **Yes** | Your Telegram API Hash from [my.telegram.org](https://my.telegram.org) |
| `LOG_CHANNEL` | No | Optional: Channel ID for logging bot activity (format: `-100xxxxxxxxxx`) |

</details>

## Screenshots/Demo

<details>
  <summary><strong>View Bot Interface</strong></summary>

  <br>
  <p align="center">
    <kbd>
      <img width="600" src="demo.jpg" alt="Demo">
    </kbd>
  </p>

</details>
