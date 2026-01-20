import base64
import json
import sys
from collections import deque
from pathlib import Path


def assign_node_ids(node):
    counter = 0
    queue = deque([node])

    while queue:
        node = queue.popleft()
        counter += 1
        node["_id"] = counter
        for child in node.get("children", []):
            queue.append(child)

    return node


def find_path_to_text(node, target_text, current_path="", node_ids=None):
    if node_ids is None:
        node_ids = []

    current_text = current_path + node.get("text", "")
    current_ids = node_ids + [node["_id"]]

    # Check if target is found in current path
    if target_text.lower() in current_text.lower():
        return current_ids, current_text

    # Recurse into children
    for child in node.get("children", []):
        result = find_path_to_text(child, target_text, current_text, current_ids)
        if result:
            return result

    return None


def find_branch_paths(node, current_path=None, current_text="", branch_counter=None):
    if current_path is None:
        current_path = []
    if branch_counter is None:
        branch_counter = {"value": 0}

    branches = []
    current_path = current_path + [node["_id"]]
    current_text = current_text + node.get("text", "")

    children = node.get("children", [])

    if not children:
        branch_counter["value"] += 1
        branches.append(
            {
                "branch": branch_counter["value"],
                "path": current_path.copy(),
                "text": current_text,
            }
        )
    else:
        for child in children:
            child_branches = find_branch_paths(
                child, current_path, current_text, branch_counter
            )
            branches.extend(child_branches)

    return branches


def path_to_hash(node_ids):
    ids_str = ",".join(str(id) for id in node_ids)
    return base64.b64encode(ids_str.encode()).decode().rstrip("=")


def load_tree(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    tree_data = data.get("tree", data)
    assign_node_ids(tree_data)
    return tree_data


def search_text(json_path):
    print(f"\n📄 Loaded: {json_path}")
    tree = load_tree(json_path)

    print("\nEnter text to search for (or 'quit' to exit):")
    print("The script will find the path to the first node containing that text.\n")

    while True:
        print("-" * 60)
        print("🔍 Search (Press Ctrl+D or Ctrl+Z to submit):")
        target = sys.stdin.read().strip()
        if target.lower() in ("quit", "q", "exit"):
            break

        if not target:
            continue

        result = find_path_to_text(tree, target)
        if result:
            ids, matched_text = result
            hash_value = path_to_hash(ids)
            print(f"\n✅ Found!")
            print(f"   Node IDs: {ids}")
            print(f"   Hash: {hash_value}")
            if len(matched_text) > 300:
                print(f"\n   Matched text (last 300 chars):")
                print(f"   ...{matched_text[-300:]}\n")
            else:
                print(f"\n   Matched text:")
                print(f"   {matched_text}\n")
        else:
            print(f"\n❌ Text not found in tree\n")


def main():
    json_path = sys.argv[1]

    if not Path(json_path).exists():
        print(f"❌ File not found: {json_path}")
        sys.exit(1)

    search_text(json_path)


if __name__ == "__main__":
    main()
