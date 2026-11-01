"""Clean code - Remove excessive comments and emojis."""
import os
import re
from pathlib import Path

REPLACEMENTS = [
    # Vietnamese to English comments
    (r'"""[^"]*Học tập từ P-041[^"]*"""', ''),
    (r'# Vietnamese comments', ''),
    
    # Remove emojis
    (r'[✅❌⚠️🔥💡📚🎯🚀🏥📦🔍📊⏳🎓✨👋📋🤖🔧🎉⭐📍]', ''),
    
    # Clean Vietnamese comments
    (r'""".*Học tập.*?"""', ''),
    (r'# .*á$', ''),
    (r'Đã\s+', ''),
    (r'đã\s+', ''),
    (r'của\s+', ''),
    (r'cho\s+', ''),
    (r'với\s+', ''),
    (r'khi\s+', ''),
    (r'nếu\s+', ''),
    (r'là\s+', ''),
]

def clean_file(filepath: Path) -> bool:
    """Clean a single Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Remove emojis
        content = re.sub(r'[✅❌⚠️🔥💡📚🎯🚀🏥📦🔍📊⏳🎓✨👋📋🤖🔧🎉⭐📍🏗️📡💬🛡️🔄📈📝🎨]', '', content)
        
        # Clean excessive comments
        lines = content.split('\n')
        cleaned_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            # Skip empty comment lines
            if line.strip() == '#' or line.strip() == '"""':
                continue
            
            # Skip long Vietnamese docstrings
            if '"""' in line and any(vn in line for vn in ['Học tập', 'đã', 'của', 'cho', 'với']):
                if line.count('"""') == 2:
                    continue
                else:
                    skip_next = not skip_next
                    continue
            
            if skip_next:
                if '"""' in line:
                    skip_next = False
                continue
            
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Remove multiple blank lines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error cleaning {filepath}: {e}")
        return False


def main():
    """Clean all Python files in src/."""
    src_dir = Path('src')
    
    if not src_dir.exists():
        print("src/ directory not found")
        return
    
    cleaned_count = 0
    
    for filepath in src_dir.rglob('*.py'):
        if clean_file(filepath):
            print(f"Cleaned: {filepath}")
            cleaned_count += 1
    
    print(f"\nCleaned {cleaned_count} files")


if __name__ == '__main__':
    main()
