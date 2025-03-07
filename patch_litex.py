import re
import shutil
import site
from pathlib import Path

def find_core_file():
    """Locate core.py in LiteX installation"""
    try:
        import litex
        litex_path = Path(litex.__file__).parent
        core_path = litex_path / "soc" / "cores" / "cpu" / "zynq7000" / "core.py"
        return core_path if core_path.exists() else None
    except ImportError:
        pass

    # Search site-packages directories
    for pkg_dir in site.getsitepackages():
        candidate = Path(pkg_dir) / "litex" / "soc" / "cores" / "cpu" / "zynq7000" / "core.py"
        if candidate.exists():
            return candidate
    return None

def modify_axi_hp_slave(content):
    """Modify function with format-preserving replacement"""
    modified = False
    pos = 0  # Track processing position

    # Stage 1: Add data_width parameter to method signature
    method_def_re = re.compile(
        r'(def\s+add_axi_hp_slave\()(.*?)(\)\s*:)',
        re.DOTALL
    )
    match = method_def_re.search(content, pos)
    if not match:
        print("[Error] add_axi_hp_slave method not found")
        return content, False

    params = match.group(2)
    if 'data_width' not in params:
        # Add parameter with proper comma placement
        new_params = params.rstrip()
        if new_params and not new_params.endswith(','):
            new_params += ','
        new_params += ' data_width=64'
        
        # Update content and position
        content = content[:match.start(2)] + new_params + content[match.end(2):]
        modified = True
        pos = match.end() + (len(new_params) - len(params))
        print("[Parameter] Added data_width=64")
    else:
        pos = match.end()
        print("[Parameter] data_width already exists")

    # Stage 2: Modify AXIInterface call with whitespace preservation
    axi_call_re = re.compile(
        r'(axi\.AXIInterface\()(.*?)(data_width)\s*([=])\s*64(.*?)(\))',
        re.DOTALL
    )
    match = axi_call_re.search(content, pos)
    if match:
        # Rebuild call with original whitespace
        new_call = (
            f"{match.group(1)}{match.group(2)}"
            f"{match.group(3)}{match.group(4)}data_width"
            f"{match.group(5)}{match.group(6)}"
        )
        content = content[:match.start()] + new_call + content[match.end():]
        modified = True
        print("[AXI Call] Modified with original formatting")
    else:
        print("[AXI Call] No target found for modification")

    return content, modified

def main():
    core_path = find_core_file()
    if not core_path:
        print("Error: core.py not found")
        return

    # Create backup
    backup_path = core_path.with_suffix(".py.bak")
    shutil.copy(core_path, backup_path)
    print(f"Backup created: {backup_path}")

    # Read and modify
    with open(core_path, "r+", encoding="utf-8") as f:
        content = f.read()
        new_content, modified = modify_axi_hp_slave(content)
        
        if modified:
            f.seek(0)
            f.truncate()
            f.write(new_content)
            print("Modification successful")
        else:
            print("No changes made")

if __name__ == "__main__":
    main()