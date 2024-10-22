def read_file(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
    return content

def write_file(file_path, content):
    with open(file_path, 'w') as f:
        f.writelines(content)

def remove_comments(file_path, output_path):
    lines = read_file(file_path)
    filtered_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
    write_file(output_path, filtered_lines)

def replace_values_with_mapping(original_file_path, mapping_file_path):
    original_content = read_file(original_file_path)
    mapping_content = read_file(mapping_file_path)

    mapping = {}
    for line in mapping_content:
        key, value = line.strip().split('=', 1)
        mapping[key] = value

    updated_content = []
    for line in original_content:
        key, value = line.strip().split('=', 1)
        if key in mapping:
            updated_content.append(f"{key}={mapping[key]}\n")
        else:
            updated_content.append(line)

    write_file(original_file_path, updated_content)


original_file_path = '.env'
mapping_file_path = '.tmp.env'

remove_comments(".env.example", ".env")
replace_values_with_mapping(original_file_path, mapping_file_path)


