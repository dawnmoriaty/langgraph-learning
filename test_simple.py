"""
Script để test simple example mà không cần chạy server
Giúp bạn hiểu LangGraph trước khi dùng API
"""
import sys
import os

# Thêm project root vào Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.agents.simple_example import run_simple_example

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║            📚 LangGraph Simple Example                   ║
╚══════════════════════════════════════════════════════════╝

Đây là example cơ bản nhất về LangGraph.
Không cần API key, không cần LLM.
Chỉ để hiểu cách graph hoạt động.

""")
    
    try:
        result = run_simple_example()
        print("\n✅ Example chạy thành công!")
        print("\nĐây là flow cơ bản:")
        print("  START -> Node1 -> Node2 -> Node3 -> END")
        print("\nMỗi node nhận state, xử lý, và return state mới.")
        print("LangGraph tự động merge các state lại với nhau.\n")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
