"""Clean all Vietnamese text from source code."""
import re
from pathlib import Path

REPLACEMENTS = {
    # Common Vietnamese phrases to English
    'với fallback': 'with fallback',
    'cho ': 'for ',
    'của ': 'of ',
    'với ': 'with ',
    'đã ': '',
    'nếu ': 'if ',
    'khi ': 'when ',
    'không có': 'no',
    'không ': 'not ',
    'Không có': 'No',
    'Hãy set': 'Set',
    'ít nhất một': 'at least one',
    'hoặc ': 'or ',
    'từng ': 'each ',
    'tất cả ': 'all ',
    'mỗi ': 'each ',
    'toàn bộ ': 'entire ',
    'Thực hiện ': 'Execute ',
    'Tách biệt ': 'Separate ',
    'Lấy ': 'Get ',
    'Dùng ': 'Use ',
    'trong ': 'in ',
    'rồi ': 'then ',
    'nhưng ': 'but ',
    'Có ': 'Have ',
    'Bạn ': 'You ',
    'vào ': 'to ',
    'Check health của': 'Check health of',
    'nào available': 'available',
    'provider nào': 'providers',
    'API key.': 'API key',
}

def clean_file(filepath: Path) -> bool:
    """Clean Vietnamese text from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Apply replacements
        for vn, en in REPLACEMENTS.items():
            content = content.replace(vn, en)
        
        # Clean specific patterns
        content = re.sub(r'Service layer for[^"]*functionality', 'Service layer for functionality', content)
        content = re.sub(r'Handler for[^"]*subclasses', 'Handler for AppError subclasses', content)
        content = re.sub(r'Response with[^"]*pagination', 'Response with pagination', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error: {filepath}: {e}")
        return False

def main():
    """Clean all Python files."""
    src_dir = Path('src')
    cleaned = 0
    
    for filepath in src_dir.rglob('*.py'):
        if clean_file(filepath):
            print(f"Cleaned: {filepath}")
            cleaned += 1
    
    print(f"\nCleaned {cleaned} files")

if __name__ == '__main__':
    main()
