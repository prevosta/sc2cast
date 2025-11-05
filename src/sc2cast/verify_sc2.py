"""Verify StarCraft II installation on Windows."""

from pathlib import Path


def find_sc2_installation():
    """Check common SC2 installation locations."""
    possible_paths = [
        Path("C:/Program Files (x86)/StarCraft II"),
        Path("C:/Program Files/StarCraft II"),
        Path.home() / "Games" / "StarCraft II",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None


if __name__ == "__main__":
    sc2_path = find_sc2_installation()
    
    if sc2_path:
        print(f"✅ SC2 found at: {sc2_path}")
        print(f"✅ SC2 executable exists: {(sc2_path / 'StarCraft II.exe').exists()}")
    else:
        print("❌ SC2 not found in common locations!")
        print("Please verify your StarCraft II installation.")
