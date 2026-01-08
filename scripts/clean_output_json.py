import json
import os


def remove_key_recursive(data, key_to_remove):
    """
    Recursively removes a key from a nested dictionary or list of dictionaries.
    """
    if isinstance(data, dict):
        keys_to_delete = [k for k in data if k == key_to_remove]
        for k in keys_to_delete:
            del data[k]

        for k, v in data.items():
            remove_key_recursive(v, key_to_remove)

    elif isinstance(data, list):
        for item in data:
            remove_key_recursive(item, key_to_remove)


def get_json_size(data):
    """Returns the size of the JSON object as a string in bytes."""
    return len(json.dumps(data).encode("utf-8"))


if __name__ == "__main__":
    files = os.listdir("token_tree_analysis/sample_outputs")
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join("token_tree_analysis/sample_outputs", file)
            with open(file_path, "r") as f:
                data = json.load(f)

            initial_size = get_json_size(data)

            remove_key_recursive(data, "full_text")

            final_size = get_json_size(data)
            space_freed = initial_size - final_size

            with open(file_path, "w") as f:
                json.dump(data, f)

            print(f"Cleaned File: {file}")
            print(f"\tInitial Size: {initial_size} bytes")
            print(f"\tFinal Size:   {final_size} bytes")
            print(f"\t------------------------------------")
            print(
                f"\tTotal Space Freed: {space_freed} bytes ({space_freed / 1024:.2f} KB)\n"
            )
