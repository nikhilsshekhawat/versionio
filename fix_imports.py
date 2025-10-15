# fix_imports.py
import os

print("Fixing import issues...")

# Fix 1: Update wrapper.py
wrapper_file = 'src/versionio/wrapper.py'
print(f"Fixing {wrapper_file}...")

with open(wrapper_file, 'r') as f:
    lines = f.readlines()

# Fix the imports
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    
    # Remove list_versions from utils import
    if 'list_versions' in line and 'from versionio.utils import' in lines[i-1] if i > 0 else False:
        continue  # Skip this line
    
    # Add import in _apply_retention_policy method
    if 'def _apply_retention_policy' in line:
        new_lines.append(line)
        # Find the right place to add the import
        for j in range(i+1, min(i+10, len(lines))):
            new_lines.append(lines[j])
            if 'if self._policy.max_versions is None:' in lines[j]:
                new_lines.append(lines[j+1])  # Add the return line
                new_lines.append('        \n')
                new_lines.append('        # Import here to avoid circular import\n')
                new_lines.append('        from versionio.version import list_versions\n')
                skip_next = True
                break
    elif i < len(lines) - 1:
        new_lines.append(line)

# Write back
with open(wrapper_file, 'w') as f:
    f.writelines(new_lines)

print(f"✓ Fixed {wrapper_file}")

# Fix 2: Clean test_versionedfile.py
test_file = 'tests/test_versionedfile.py'
print(f"Fixing {test_file}...")

if os.path.exists(test_file):
    with open(test_file, 'r') as f:
        content = f.read()
    
    # Remove any markdown fences
    content = content.replace('```', '')
    
    # Make sure file ends properly
    content = content.rstrip() + '\n'
    
    with open(test_file, 'w') as f:
        f.write(content)
    
    print(f"✓ Fixed {test_file}")

print("\nFixes applied! Now run: pytest")