# My IPX800 V3

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

 <!--
Uncomment and customize these badges if you want to use them:
[![Discord][discord-shield]][discord]
-->

**✨ Develop in the cloud:** Want to contribute or customize this integration? Open it directly in GitHub Codespaces - no local setup required!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/amg0/ha_ipx800v3?quickstart=1)

## ✨ Caveats

this is my first custom integration on HomeAssistant and I am fully leveraging the excellent integration template from: <https://github.com/jpawlowski/hacs.integration_blueprint> so many thanks to him

At this point, not everything is fully tested or in a stable final version, use at your own risk and please accept evolutions as I grow myself in home assistant custom integration understanding.

HACS integration is not done yet. please Ignore any reference to HACS on this page for now and just use this repo directly into Home Assistant as a custom repo.

Feature under progress:

- **HACS**: HACS integration not made yet

## ✨ Features

- **Easy Setup**: Simple configuration through the UI - no YAML required
- **Configuration**: hostname, port, user and password
- **Optimized Polling**: only one API call for all entities/sensors and configurable refresh rate
- **Push mode**: wip, not yet fully functional , IPX will be able to push changes into Home assistant for real time updates
- **Diagnostic Info**: View filter life, runtime hours, and device statistics
- **Reconfigurable**: Change credentials anytime without removing the integration
- **Options Flow**: Adjust settings like update interval after setup
- **Custom Services**: Advanced control with built-in service calls
- **Push mode**: wip, not yet fully functional , IPX will be able to push changes into Home assistant for real time updates.

**This integration will set up the following platforms.**

| Platform        | Description            |
| --------------- | ---------------------- |
| `sensor`        | Analog Sensor, Counter |
| `binary_sensor` | Digital Input          |
| `switch`        | Output Relays          |

> [!TIP]
> **Names:** An integration option controls if the names of entities is imported from the names of the relay/input/sensor of the IPX board

## 🚀 Quick Start

### Step 1: Install the Integration

**Prerequisites:** This integration requires [HACS](https://hacs.xyz/) (Home Assistant Community Store) to be installed.

Click the button below to open the integration directly in HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=jpawlowski&repository=ha_ipx800v3&category=integration)

Then:

1. Click "Download" to install the integration
2. **Restart Home Assistant** (required after installation)

> [!NOTE]
> The My Home Assistant redirect will first take you to a landing page. Click the button there to open your Home Assistant instance.

<details>
<summary><strong>Manual Installation (Advanced)</strong></summary>

If you prefer not to use HACS:

1. Download the `custom_components/my_ipx800v3/` folder from this repository
2. Copy it to your Home Assistant's `custom_components/` directory
3. Restart Home Assistant

</details>

### Step 2: Add and Configure the Integration

**Important:** You must have installed the integration first (see Step 1) and restarted Home Assistant!

#### Option 1: One-Click Setup (Quick)

Click the button below to open the configuration dialog:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=my_ipx800v3)

Follow the setup wizard:

> [!TIP]
> Look at the webhook url at the top of the parameter dialog box, copy paste it to configure your IPX800 board Push Url. this is optional but better for near real time updates

1. Enter your ipx board hostname or ip address
2. Enter your port ( 80 by default )
3. Chose if you want to import the names from the IPX board
4. optionally enter a user name
5. and a password if your IPX is configured with a user/pwd security
6. Click Submit

That's it! The integration will start loading your data.

#### Option 2: Manual Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for "My IPX800 V3"
4. Follow the same setup steps as Option 1

### Step 3: Adjust Settings (Optional)

After setup, you can adjust options:

1. Go to **Settings** → **Devices & Services**
2. Find **My IPX800 V3**
3. Click **Configure** to adjust:
   - Update interval (how often to refresh data)

You can also **Reconfigure** your board and chose to change the import name options ( it will impact your entities names but not the ID )

### Step 4: Start Using!

The integration creates several entities for your IPX800 V3 board

- **Sensors**: Analog sensors, Counter
- **Binary Sensors**: Digital Inputs
- **Switches**: Output relays

Find all entities in **Settings** → **Devices & Services** → **My IPX800 V3** → click on the device.

## Available Entities

### Sensors

- **Analog**: the type of analog sensor is retrieved directly from the IPX configuration on the IPX board and the calculation for the native value is made according to the same calculation that the IPX board does itself.

### Binary Sensors

- **Digital Input**: Reflects and control the states of digital inputs on the board. there is also an API health sensor that tells if the connection is established

### Switches

- **Output Relays**: Reflects and control the states on the board

## Custom Services

The integration provides services for advanced automation:

### `my_ipx800v3.reload_data`

Manually refresh data from the API without waiting for the update interval.
Takes a target device as parameter ( so it applies to the IPX800 boar, not the entities ).
You can use developer tools Action page to test with the UI form and device selector, or use the yaml way

**Example:**

```yaml
action: my_ipx800v3.reload_data
data: {}
target:
  device_id: your_device_id like 8723064826443c1c71e4177d2204eae9
```

Use these services in automations or scripts for more control.

## Configuration Options

### During Setup

| Name         | Required | Description                                         |
| ------------ | -------- | --------------------------------------------------- |
| Host         | Yes      | hostname or IP address                              |
| Post         | Yes      | IPX board port number - defaults to 80              |
| Import Names | Yes      | if ON, it will import the entity names from the ipx |
| Username     | No       | Your account username                               |
| Password     | No       | Your account password                               |

### After Setup (Options)

You can change these anytime by clicking **Configure**:

| Name            | Default | Description               |
| --------------- | ------- | ------------------------- |
| Update Interval | 30 s    | How often to refresh data |

## Troubleshooting

### Authentication Issues

#### Reauthentication

If your credentials expire or change, Home Assistant will automatically prompt you to reauthenticate:

1. Go to **Settings** → **Devices & Services**
2. Look for **"Action Required"** or **"Configuration Required"** message on the integration
3. Click **"Reconfigure"** or follow the prompt
4. Enter your updated credentials
5. Click Submit

The integration will automatically resume normal operation with the new credentials.

#### Manual Credential Update

You can also update credentials at any time without waiting for an error:

1. Go to **Settings** → **Devices & Services**
2. Find **My IPX800 V3**
3. Click the **3 dots menu** → **Reconfigure**
4. Enter new username/password
5. Click Submit

#### Connection Status

Monitor your connection status with the **API Connection** binary sensor:

- **On** (Connected): Integration is receiving data normally
- **Off** (Disconnected): Connection lost or authentication failed
  - Check the binary sensor attributes for diagnostic information
  - Verify credentials if authentication failed
  - Check network connectivity

### Enable Debug Logging

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.my_ipx800v3: debug
```

### Common Issues

#### Authentication Errors

If you receive authentication errors:

1. Verify your username and password are correct
2. Check that your account has the necessary permissions
3. Wait for the automatic reauthentication prompt, or manually reconfigure
4. Check the API Connection binary sensor for status

#### Device Not Responding

If your device is not responding:

1. Check the **API Connection** binary sensor - it should be "On"
2. Check your network connection
3. Verify the device is powered on
4. Check the integration diagnostics (Settings → Devices & Services → My IPX800 V3 → 3 dots → Download diagnostics)

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request if you have suggestions or improvements.

You have two options to set up a development environment — expand below for full details.

<details>
<summary><strong>Development Setup</strong></summary>

Both options provide the same fully-configured environment with Home Assistant, Python 3.14, Node.js LTS, and all necessary tools.

### Option 1: GitHub Codespaces ☁️

Develop directly in your browser without installing anything locally!

1. Click the green **"Code"** button in this repository
2. Switch to the **"Codespaces"** tab
3. Click **"Create codespace on main"**
4. **Wait for setup** (2-3 minutes first time) — everything installs automatically
5. **Review and commit** your changes in the Source Control panel (`Ctrl+Shift+G`)

> [!TIP]
> Codespaces gives you **60 hours/month free** for personal accounts. When you start Home Assistant (`script/develop`), port 8123 forwards automatically.

### Option 2: Local Development with VS Code (Recommended) 💻

#### Prerequisites

You'll need these installed locally:

- **A Docker-compatible container engine** — see options by platform:

  | Option                                                                                                                   | 🍎 macOS | 🐧 Linux | 🪟 Windows | Notes                                                                                                                                                                                                                                     |
  | ------------------------------------------------------------------------------------------------------------------------ | :------: | :------: | :--------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | [Docker Desktop](https://www.docker.com/products/docker-desktop/)                                                        |    ✅    |    ✅    |     ✅     | **Easiest starting point for all platforms.** GUI-based, well-documented, one installer. Uses WSL2 as default backend on Windows (Hyper-V also available). Installation requires admin rights; daily use does not. Free for personal use. |
  | [OrbStack](https://orbstack.dev/) ⭐                                                                                     |    ✅    |    —     |     —      | **Recommended for macOS** once Docker Desktop feels slow. Starts in ~2s, much lighter on RAM/CPU, full Docker API compatibility. Free for personal use.                                                                                   |
  | [Docker CE](https://docs.docker.com/engine/install/) (native) ⭐                                                         |    —     |    ✅    |     —      | **Recommended for Linux.** Install directly via your package manager — no VM, no GUI, no overhead. Free.                                                                                                                                  |
  | [WSL2](https://learn.microsoft.com/windows/wsl/install) + [Docker CE](https://docs.docker.com/engine/install/ubuntu/) ⭐ |    —     |    —     |     ✅     | **Recommended for Windows** once you're comfortable with WSL2. Docker runs natively inside WSL2 — no GUI overhead. Requires one-time WSL2 setup. Free.                                                                                    |
  | [Rancher Desktop](https://rancherdesktop.io/)                                                                            |    ✅    |    ✅    |     ✅     | Open source by SUSE. GUI-based, uses WSL2 on Windows. Good alternative to Docker Desktop. Free.                                                                                                                                           |
  | [Colima](https://github.com/abiosoft/colima)                                                                             |    ✅    |    ✅    |     —      | CLI-only, very lightweight. Good for terminal-focused workflows. Free.                                                                                                                                                                    |

- **VS Code** with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- **Git** — macOS and Linux usually have it already; see below if not, or to get a newer version:
  - **🍎 macOS:** The system Git (`xcode-select --install`) works fine. Recommended: `brew install git` ([Homebrew](https://brew.sh/)) for a current version.
  - **🐧 Linux:** Usually pre-installed. If not: `sudo apt install git` (or your distro's equivalent).
  - **🪟 Windows + WSL2 ⭐:** Install Git _inside WSL2_ with `sudo apt install git`. Git on Windows itself is not needed — VS Code clones and operates entirely within WSL2.
  - **🪟 Windows + Docker Desktop:** Install via `winget install Git.Git` or download [Git for Windows](https://git-scm.com/download/win).
- **Hardware** — the devcontainer runs a full Home Assistant instance including Python tooling:

  |          | Minimum    | Recommended                           |
  | -------- | ---------- | ------------------------------------- |
  | **RAM**  | 8 GB       | 16 GB or more                         |
  | **CPU**  | 4 cores    | 8 cores or more                       |
  | **Disk** | 10 GB free | 20 GB free (SSD strongly recommended) |

> [!TIP]
> **Not sure which Docker option to pick?** Start with [Docker Desktop](https://www.docker.com/products/docker-desktop/) — it works on all platforms, has a GUI, and needs no extra setup. The ⭐ options are faster alternatives once you're comfortable. macOS and Linux offer the best devcontainer experience — containers run with no extra VM layer and file I/O is fast. Windows works well too; this integration uses named container volumes (files live inside WSL2, not on the Windows drive) to keep performance acceptable.

> [!NOTE]
> **New to Dev Containers?** See the [VS Code Dev Containers documentation](https://code.visualstudio.com/docs/devcontainers/containers#_system-requirements) for system requirements and how to install the extension. **Once the extension is installed, you're done** — this repository already ships a complete devcontainer configuration. You don't need to follow the rest of the VS Code guide; the setup steps below are all that's needed.

#### Setup Steps

1. **Clone in a Dev Container:**

   **🍎 macOS / 🐧 Linux:** Clone the repository and open the folder in VS Code → click **"Reopen in Container"** when prompted (or `F1` → **"Dev Containers: Reopen in Container"**).

   **🪟 Windows:** In VS Code, press `F1` → **"Dev Containers: Clone Repository in Named Container Volume..."** and enter the repository URL. This keeps files inside WSL2 for best I/O performance.

2. Wait for the container to build (2-3 minutes first time)

3. **Review and commit** changes in Source Control (`Ctrl+Shift+G`)

4. **Start developing**:

   ```bash
   script/develop  # Home Assistant runs at http://localhost:8123
   ```

> [!NOTE]
> Both Codespaces and local DevContainer provide the exact same experience. The only difference is where the container runs (GitHub's cloud vs. your machine).

</details>

---

## 🤖 AI-Assisted Development

> [!NOTE]
> **Transparency Notice:** This integration was developed with assistance from AI coding agents (GitHub Copilot, Claude, and others). While the codebase follows Home Assistant Core standards, AI-generated code may not be reviewed or tested to the same extent as manually written code. AI tools were used to generate boilerplate code, implement standard integration features (config flow, coordinator, entities), ensure code quality and type safety, and write documentation. If you encounter unexpected behavior, please [open an issue](../../issues) on GitHub.
>
> _This section can be removed or modified if AI assistance was not used in your integration's development._

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [@amg0][user_profile]**

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/amg0/ha_ipx800v3.svg?style=for-the-badge
[commits]: https://github.com/amg0/ha_ipx800v3/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/amg0/ha_ipx800v3.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40amg0-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/amg0/ha_ipx800v3.svg?style=for-the-badge
[releases]: https://github.com/amg0/ha_ipx800v3/releases
[user_profile]: https://github.com/jpawlowski
[buymecoffee]: https://buymeacoffee.com/amg0
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge

<!-- Optional badge definitions - uncomment if needed:
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
-->
