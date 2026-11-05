"""Intent of each stroke line, as the comment above it in the script says (see answers-step2.md, Question 3).
L: meant to read (a light, an edge, a glint, a dark accent). F: meant faint (signatures, grain lines).
B: a broad modelling pass (wide bristle, laid to shift a value part of the way).
G: the bookcases' gilt, "faded gilt: small, few, varied" -- meant to be seen, faintly."""
INTENT = {
    "beyond_doorway.py": {29: "B", 35: "B", 41: "B", 71: "L", 77: "F"},
    "desk.py": {40: "F", 46: "B", 49: "L", 51: "F", 52: "F", 53: "L", 54: "F", 55: "F", 59: "L", 63: "F"},
    "counter.py": {34: "F", 37: "B", 40: "L", 44: "F"},
    "shelves.py": {75: "L", 76: "L", 83: "G", 86: "G", 90: "F"},
    "doorway_wall.py": {34: "B", 38: "B", 77: "L", 79: "L", 82: "B", 87: "F"},
    "locked_shelf.py": {51: "L", 53: "L", 56: "L", 57: "L", 59: "L", 63: "L", 64: "L", 68: "F"},
    "patron_default.py": {67: "L", 71: "L", 72: "L", 73: "L", 77: "F"},
    "candle.py": {45: "L", 46: "L", 47: "L", 48: "L", 52: "L", 53: "L", 56: "L", 57: "L", 58: "L", 59: "L", 63: "F"},
}
