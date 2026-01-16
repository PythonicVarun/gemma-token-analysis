import json
import os
from pathlib import Path


def extract_all_branches(node, current_path=""):
    branches = []

    current_text = current_path + node.get("text", "")
    children = node.get("children", [])

    if not children or len(children) == 0:
        if current_text:
            return [current_text]
        return []

    for child in children:
        child_branches = extract_all_branches(child, current_text)
        branches.extend(child_branches)

    return branches


def process_json_file(json_path, output_dir):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict) and 'tree' in data:
            tree_data = data['tree']
        else:
            tree_data = data

        branches = extract_all_branches(tree_data)

        input_filename = Path(json_path).stem
        output_path = os.path.join(output_dir, f"{input_filename}_branches.txt")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Source: {json_path}\n")

            if isinstance(data, dict) and 'metadata' in data:
                f.write(f"Prompt: {data['metadata'].get('prompt', 'N/A')}\n")

            f.write(f"Total branches: {len(branches)}\n")
            f.write("=" * 80 + "\n\n")

            if len(branches) == 0:
                f.write("WARNING: No branches found!\n")
                f.write("This might indicate an issue with the JSON structure.\n")
            else:
                for i, branch in enumerate(branches, 1):
                    f.write(f"Branch {i}:\n")
                    f.write("-" * 80 + "\n")
                    f.write(branch + "\n")
                    f.write("-" * 80 + "\n\n")

        print(f"  :) Processed {json_path}")
        print(f"  Found {len(branches)} branches")
        print(f"  Output: {output_path}")

        if len(branches) == 0:
            print(f"  WARNING: No branches extracted! Check JSON structure.")
        print()

        return len(branches)

    except Exception as e:
        print(f"✗ Error processing {json_path}: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 0


def inspect_json_structure(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\n{'='*80}")
        print(f"Inspecting: {json_path}")
        print(f"{'='*80}")

        def print_structure(obj, indent=0, max_depth=3):
            if indent > max_depth:
                return

            prefix = "  " * indent
            if isinstance(obj, dict):
                print(f"{prefix}Dict with keys: {list(obj.keys())}")
                for key in list(obj.keys())[:5]:
                    print(f"{prefix}  '{key}':")
                    print_structure(obj[key], indent + 2, max_depth)
            elif isinstance(obj, list):
                print(f"{prefix}List with {len(obj)} items")
                if len(obj) > 0:
                    print(f"{prefix}  First item:")
                    print_structure(obj[0], indent + 2, max_depth)
            else:
                value_str = str(obj)[:80]
                print(f"{prefix}Value: {value_str}")

        print_structure(data)
        print()

    except Exception as e:
        print(f"Error inspecting {json_path}: {str(e)}\n")


def process_directory(input_dir, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(input_dir, "extracted_branches")

    os.makedirs(output_dir, exist_ok=True)
    json_files = list(Path(input_dir).glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return

    print(f"Found {len(json_files)} JSON file(s)\n")
    print("=" * 80)
    print()

    total_branches = 0
    processed_count = 0

    for json_file in json_files:
        branches = process_json_file(json_file, output_dir)
        if branches > 0:
            processed_count += 1
            total_branches += branches

    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Files processed: {processed_count}/{len(json_files)}")
    print(f"  Total branches extracted: {total_branches}")
    print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_directory = sys.argv[1]
    else:
        input_directory = "."

    output_directory = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Processing JSON files in: {input_directory}\n")
    process_directory(input_directory, output_directory)
