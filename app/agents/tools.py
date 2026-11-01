"""
Tools cho LangGraph Agent
Đây là các function mà agent có thể gọi
"""
from langchain_core.tools import tool


@tool
def add(a: float, b: float) -> float:
    """Cộng hai số lại với nhau.
    
    Args:
        a: Số thứ nhất
        b: Số thứ hai
        
    Returns:
        Tổng của a và b
    """
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Trừ hai số.
    
    Args:
        a: Số bị trừ
        b: Số trừ
        
    Returns:
        Hiệu của a và b
    """
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Nhân hai số.
    
    Args:
        a: Số thứ nhất
        b: Số thứ hai
        
    Returns:
        Tích của a và b
    """
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Chia hai số.
    
    Args:
        a: Số bị chia
        b: Số chia
        
    Returns:
        Thương của a và b
        
    Raises:
        ValueError: Nếu b = 0
    """
    if b == 0:
        raise ValueError("Không thể chia cho 0!")
    return a / b


# Danh sách tất cả tools
ALL_TOOLS = [add, subtract, multiply, divide]
