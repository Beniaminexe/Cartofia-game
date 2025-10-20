
# 🕹️ Cartofia

**Cartofia** is a retro-inspired 2D platformer built with [Pygame](https://www.pygame.org/).  
Run, jump, and collect coins across multiple levels while dodging enemies and hazards.  
Originally inspired by [russs123’s Platformer project](https://github.com/russs123/Platformer),  
Cartofia expands and refines that foundation with fullscreen support, sound polish, and a new visual style.

---

## 🎮 Features

- Smooth fullscreen or windowed gameplay.  
- Animated player movement and gravity physics.  
- Moving platforms, enemies, lava, and collectible coins.  
- Level loading from external data files (`pickle`).  
- Background music and sound effects.  
- Simple main menu with Start / Exit buttons.  
- Restart functionality and multi-level progression.  

---

## 🧰 Requirements

| Dependency | Version | Notes |
|-------------|----------|-------|
| Python | 3.10+ | Works up to 3.13 |
| Pygame | 2.6.1 | Required for rendering, input, and audio |

---

## ⚙️ Installation

Clone the repository and install dependencies:
```bash
git clone https://github.com/Beniaminexe/Cartofia-game.git
cd Cartofia-game
pip install pygame
````

---

## ▶️ Running the Game

```bash
python cartofia.py
```

The game launches in **fullscreen** mode.
Use **F11** to toggle fullscreen/windowed mode, and **ESC** to quit.

---

## 🎮 Controls

| Key       | Action                                         |
| --------- | ---------------------------------------------- |
| **A / D** | Move left / right                              |
| **SPACE** | Jump                                           |
| **ESC**   | Quit                                           |
| **F11**   | Toggle fullscreen                              |
| **Mouse** | Interact with buttons (Start / Exit / Restart) |

---

## 🧱 Level Data

Levels are stored as binary files named `levelX_data` (where X is the level number).
Each contains tile data serialized via Python’s `pickle` module.
You can edit or replace them to create custom levels.

---

## 🎨 Assets

All visual and audio assets are located in the `img/` directory:

* `sky.png`, `sun.png` – background art
* `dirt.png`, `grass.png` – terrain tiles
* `coin.png`, `blob.png`, `lava.png` – interactable entities
* `platform.png`, `exit.png` – game mechanics
* `music.mp3`, `coin.wav`, `jump.wav`, `game_over.wav` – sound and music

---

## 🧠 Developer Notes

Cartofia’s code demonstrates:

* Sprite-based animation
* Collision detection
* Platform physics
* Game loop architecture
* Dynamic scaling for fullscreen rendering

The game runs internally on a **1000×1000 virtual canvas**,
which is scaled to your screen resolution for consistent physics and visuals.

---

## 🧩 Roadmap

* [ ] Add settings menu (volume, difficulty, resolution)
* [ ] Add level selector
* [ ] Save high scores
* [ ] Implement parallax scrolling backgrounds
* [ ] Package via PyInstaller for distribution

---

## 📸 Screenshots



![Main Menu](img/screenshots/menu.png)
![Gameplay](img/screenshots/gameplay.png)

---

## 🧾 Credits & Attribution

Cartofia is heavily inspired by the open-source
[Platformer project by russs123](https://github.com/russs123/Platformer).

Core gameplay structure, asset layout, and level serialization originate from that project.
All modifications, new features, and design improvements are © 2025 **Beniaminexe**,
released under the same MIT License.

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👾 Author

Developed by **[Beniaminexe](https://github.com/Beniaminexe)**
Built with 💻 Python and ❤️ curiosity.


---


