# Air Pong Game with Real Hand Control

## Overview
Air Pong is an interactive game that allows players to control a paddle using hand movements. The game is inspired by the classic Pong game, where players aim to keep the ball in play by moving their paddle in response to their hand's position.

## Features
- **Hand Tracking**: Utilizes MediaPipe for accurate hand tracking, allowing for real-time control of the paddle.
- **Game Rendering**: Built with OpenCV, the game renders graphics and handles collision detection between the ball and the paddle.

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd air-pong-game
pip install -r requirements.txt
```

## Usage
Run the main application to start the game:

```bash
python src/main.py
```

Ensure your camera is enabled for hand tracking to work effectively.

## Testing
To run the unit tests for the game and hand detector, use the following command:

```bash
pytest tests/
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.