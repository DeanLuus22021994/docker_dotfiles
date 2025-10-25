#!/usr/bin/env python3
"""
Shared Colors Utility Module
Provides ANSI color codes for terminal output
"""


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'


def colorize(text: str, color: str) -> str:
    """
    Wrap text with ANSI color codes
    
    Args:
        text: Text to colorize
        color: Color attribute from Colors class (e.g., Colors.GREEN)
    
    Returns:
        Colored text with reset code
    """
    return f"{color}{text}{Colors.RESET}"


def success(text: str) -> str:
    """Return green success message"""
    return colorize(f"✓ {text}", Colors.GREEN)


def warning(text: str) -> str:
    """Return yellow warning message"""
    return colorize(f"⚠ {text}", Colors.YELLOW)


def error(text: str) -> str:
    """Return red error message"""
    return colorize(f"✗ {text}", Colors.RED)


def info(text: str) -> str:
    """Return blue info message"""
    return colorize(f"ℹ {text}", Colors.BLUE)


def bold(text: str) -> str:
    """Return bold text"""
    return colorize(text, Colors.BOLD)


def header(text: str) -> str:
    """Return bold blue header"""
    return colorize(text, f"{Colors.BOLD}{Colors.BLUE}")


def separator(width: int = 60, char: str = '=') -> str:
    """Return bold separator line"""
    return colorize(char * width, Colors.BOLD)
