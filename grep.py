import os
import re
import sys

def grep(pattern, files, recursive=False, case_sensitive=True, count_only=False,
         include=None, exclude=None, context_lines=0, invert_match=False, word_match=False):
    """
    Search for a pattern in files and print matching lines.

    Args:
    pattern (str): The pattern to search for.
    files (list): List of file paths to search in.
    recursive (bool): Flag to enable recursive search in directories.
    case_sensitive (bool): Flag to enable case-sensitive search.
    count_only (bool): Flag to display only the count of matching lines.
    include (str): Regular expression to include files for search.
    exclude (str): Regular expression to exclude files from search.
    context_lines (int): Number of lines of context to display around matches.
    invert_match (bool): Flag to invert the match, displaying non-matching lines.
    word_match (bool): Flag to search for whole words only.

    Returns:
    int: Total count of matching lines.
    """
    total_count = 0

    # Compile regular expressions for include and exclude patterns
    include_pattern = re.compile(include) if include else None
    exclude_pattern = re.compile(exclude) if exclude else None

    for file_path in files:
        if os.path.isfile(file_path):
            if include_pattern and not include_pattern.search(file_path):
                continue
            if exclude_pattern and exclude_pattern.search(file_path):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        match = re.search(pattern, line, re.IGNORECASE if not case_sensitive else 0)
                        if match and (not word_match or (word_match and re.search(r'\b{}\b'.format(pattern), line))):
                            if invert_match:
                                continue
                            if count_only:
                                total_count += 1
                                break
                            start = max(0, i - context_lines)
                            end = min(len(lines), i + context_lines + 1)
                            for j in range(start, end):
                                print(lines[j].strip())
                            total_count += 1
                            break
                        elif invert_match:
                            if count_only:
                                total_count += 1
                                break
                            start = max(0, i - context_lines)
                            end = min(len(lines), i + context_lines + 1)
                            if i < start or i >= end:
                                print(lines[i].strip())
                            total_count += 1
                            break
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        elif recursive and os.path.isdir(file_path):
            # Recursive search in directories
            sub_files = [os.path.join(file_path, f) for f in os.listdir(file_path)]
            total_count += grep(pattern, sub_files, recursive, case_sensitive, count_only,
                                 include, exclude, context_lines, invert_match, word_match)

    return total_count

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python grep.py <pattern> <file1> [<file2> ...]")
        sys.exit(1)

    pattern = sys.argv[1]
    files = sys.argv[2:]

    total_count = grep(pattern, files, recursive=True, case_sensitive=False, count_only=False,
                       include=None, exclude=None, context_lines=2, invert_match=False,
                       word_match=False)

    print(f"Total matching lines: {total_count}")
