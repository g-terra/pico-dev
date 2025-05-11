# pico-dev

A CLI tool to scaffold and manage Raspberry Pi Pico projects using Docker.

---

## ✨ Features

* Scaffold clean project folders with `Makefile` and `src/main.py`
* Uses a prebuilt Docker container (`pico-dev`) for isolated dev environments
* Accesses your Pico over USB (`/dev/ttyACM0`)
* CLI built with `typer` (supports interactive mode)

---

## 🔧 Installation

### 1. Clone the project

```bash
git clone https://github.com/g-terra/pico-dev.git
cd pico-dev
```

### 2. Install the CLI (via pipx or pip)

#### With `pipx` (recommended):

```bash
pipx install .
```

#### Or with `pip`:

```bash
pip install .
```

### 3. Build the Docker image (once)

```bash
docker build -t pico-dev .
```

---

## 🚀 Creating a New Project

You can create a new project using the interactive CLI or a direct command:

### Interactive mode:

```bash
pico-dev new
```

It will prompt:

```
Project name: my-pico-project
```

### One-liner:

```bash
pico-dev new my-pico-project
```

Result:

```
my-pico-project/
├── Makefile
└── src/
    └── main.py
```

---

## 🔌 Using the Project

Inside your project folder:

```bash
make run     # Run main.py on the Pico
make sync    # Upload code to the Pico
make list    # View Pico file tree
make clean   # Delete all files from Pico
```

> Make sure your Pico is connected at `/dev/ttyACM0`. You can override this with `DEVICE=/dev/ttyACM1 make run` if needed.

---

## 🔧 How It Works

* `Makefile` mounts your `src/` folder into a Docker container
* Docker container uses `mpremote` to interact with the Pico
* No Python files are executed on your host

---

## 📄 License

MIT

