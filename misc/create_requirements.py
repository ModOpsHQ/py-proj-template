import os
import ast

# pip install -r requirements.txt

BUILTIN_MODULES = {
    'argparse', 'ast', 'asyncio', 'json', 'logging', 
    'os', 'sys', 'typing', 're', 'math', 'datetime', 
    'collections', 'functools', 'itertools', 'pkgutil'
}

def filter_third_party_imports(imports):
    return [imp for imp in imports if imp not in BUILTIN_MODULES and not imp.startswith('src')]

def extract_all_imports(root_dir):
    imports = set()
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as file:
                    try:
                        tree = ast.parse(file.read())
                        for node in ast.walk(tree):
                            # Direct imports
                            if isinstance(node, ast.Import):
                                for n in node.names:
                                    imports.add(n.name.split('.')[0])
                            
                            # From imports
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imports.add(node.module.split('.')[0])
                    except SyntaxError:
                        print(f"Syntax error in {filepath}")
    
    return sorted(imports)

def main(print_imports=False):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_imports = extract_all_imports(project_root)
    third_party_imports = filter_third_party_imports(all_imports)
    
    if print_imports:
        print("All detected imports:")
        print("Built-in or local modules:")
        for imp in all_imports:
            if imp in BUILTIN_MODULES or imp.startswith('src'):
                print(imp)
        
        print("\nThird-party imports:")
        for imp in third_party_imports:
            print(imp)
    
    # Write to requirements.txt
    requirements_path = os.path.join(project_root, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        for imp in third_party_imports:
            f.write(f"{imp}\n")
    
    print(f"\nRequirements written to {requirements_path}")

if __name__ == "__main__":
    main(print_imports=True)