#!/usr/bin/env python3
"""
Siemens Brandville Presentation Utilities

Helper functions for working with Siemens presentation standards.
"""

from datetime import datetime
from typing import Optional

# Primary colors
SIEMENS_PETROL = "#009999"
BOLD_GREEN = "#00ffb9"
BOLD_BLUE = "#00e6dc"
DEEP_BLUE = "#000028"
LIGHT_SAND = "#f3f3f0"

# Title sizing
TITLE_SIZES = {
    "short": 80,      # <= 15 characters
    "default": 60,    # <= 35 characters
    "long": 40,       # > 35 characters
}

def get_title_size(title_text: str) -> int:
    """
    Get the appropriate title font size based on character count.

    Args:
        title_text: The title text

    Returns:
        Font size in points (80, 60, or 40)
    """
    char_count = len(title_text.strip())
    if char_count <= 15:
        return TITLE_SIZES["short"]
    elif char_count <= 35:
        return TITLE_SIZES["default"]
    else:
        return TITLE_SIZES["long"]

def get_text_colors(background: str = "dark") -> dict:
    """
    Get appropriate text colors for a given background.

    Args:
        background: "dark" (Deep Blue) or "light" (Light Sand)

    Returns:
        Dict with 'headline', 'body', 'accent' colors
    """
    if background.lower() == "dark":
        return {
            "headline": BOLD_GREEN,
            "body": LIGHT_SAND,
            "accent": BOLD_BLUE,
        }
    else:
        return {
            "headline": DEEP_BLUE,
            "body": DEEP_BLUE,
            "accent": SIEMENS_PETROL,
        }

def generate_footer(
    author: str,
    department: str,
    confidentiality: str = "Internal",
    date: Optional[str] = None,
    year: Optional[int] = None
) -> str:
    """
    Generate a properly formatted Siemens footer.

    Args:
        author: Author name
        department: Department name
        confidentiality: Confidentiality level (Public, Internal, Confidential)
        date: Date in DD.MM.YYYY format (defaults to today)
        year: Year for copyright (defaults to current year)

    Returns:
        Formatted footer string
    """
    if date is None:
        date = datetime.now().strftime("%d.%m.%Y")
    if year is None:
        year = datetime.now().year

    return f"{confidentiality} | © Siemens {year} | {author} | {department} | {date}"

def generate_contact_block(
    company: str,
    name: str,
    position: str,
    division: str,
    street: str,
    postal_code: str,
    city: str,
    phone: str,
    email: str
) -> str:
    """
    Generate properly formatted contact slide content.

    Args:
        company: Company/entity within Siemens
        name: Full name
        position: Job position
        division: Division/department
        street: Street address
        postal_code: Postal code
        city: City
        phone: Phone number
        email: Email address

    Returns:
        Formatted contact block
    """
    return f"""Publisher: Siemens {company}
{name}
{position}
{division}
{street}
{postal_code} {city}
{phone} | {email}"""

def scqa_to_slides(situation: str, complication: str, question: str, answer: str) -> dict:
    """
    Convert SCQA framework to slide content recommendations.

    Args:
        situation: The stable context
        complication: What changed / tension
        question: Key question created
        answer: Core recommendation

    Returns:
        Dict with slide type recommendations for each element
    """
    return {
        "situation": {
            "content": situation,
            "slide_type": "Content or Statement",
            "layout": "One Object Large or Statement"
        },
        "complication": {
            "content": complication,
            "slide_type": "Content or Two Columns",
            "layout": "Two Columns (before/after) or One Object Large"
        },
        "question": {
            "content": question,
            "slide_type": "Statement or Chapter Divider",
            "layout": "Statement or Chapter Divider"
        },
        "answer": {
            "content": answer,
            "slide_type": "Key Takeaways or Content",
            "layout": "Key Takeaways (recommended)"
        }
    }

def validate_color_usage(color: str, usage: str) -> tuple[bool, str]:
    """
    Validate if a color is being used appropriately.

    Args:
        color: HEX color code
        usage: Intended usage ("background", "headline", "body", "accent")

    Returns:
        Tuple of (is_valid, message)
    """
    color = color.lower()

    if usage == "background":
        valid_backgrounds = [DEEP_BLUE, LIGHT_SAND, "#ffffff", "#fff"]
        if color not in valid_backgrounds:
            return (False, f"Background should be Deep Blue (#000028) or Light Sand (#f3f3f0), not {color}")
        return (True, "Valid background color")

    elif usage == "headline":
        if color in [BOLD_GREEN, BOLD_BLUE]:
            return (True, "Valid headline color for dark background")
        elif color == SIEMENS_PETROL:
            return (True, "Valid signature color for logos/branding")
        elif color == DEEP_BLUE:
            return (True, "Valid headline color for light background")
        return (False, f"Unusual headline color: {color}")

    elif usage == "body":
        if color in [LIGHT_SAND, DEEP_BLUE]:
            return (True, "Valid body text color")
        return (False, f"Body text should be Light Sand (on dark) or Deep Blue (on light), not {color}")

    elif usage == "accent":
        valid_accents = [SIEMENS_PETROL, BOLD_BLUE, BOLD_GREEN]
        if color in valid_accents:
            return (True, "Valid accent color")
        return (False, f"Consider using Siemens Petrol (#009999) or Bold Blue (#00e6dc) for accents")

    return (False, f"Unknown usage type: {usage}")

def get_secondary_colors() -> dict:
    """
    Get secondary colors for charts and data visualization.

    Returns:
        Dict of color names and hex codes
    """
    return {
        "yellow": "#ffd732",
        "dark_yellow": "#f7c600",
        "green": "#00af8e",
        "blue": "#0087be",
        "dark_blue": "#00557c",
        "purple": "#805cff",
        "dark_purple": "#553ba3",
        "red": "#ef0137",
        "orange": "#ff9000",
        "dark_orange": "#ec6602",
    }

if __name__ == "__main__":
    # Example usage
    print("Siemens Brandville Utilities")
    print("=" * 40)

    # Title sizing example
    title = "Digital Transformation Strategy 2026"
    size = get_title_size(title)
    print(f"\nTitle: '{title}'")
    print(f"Recommended size: {size}pt")

    # Footer example
    footer = generate_footer(
        author="Max Mustermann",
        department="IT DA DO",
        confidentiality="Internal"
    )
    print(f"\nExample footer:\n{footer}")

    # Color validation
    is_valid, msg = validate_color_usage("#00ffb9", "headline")
    print(f"\nColor validation: {msg}")
