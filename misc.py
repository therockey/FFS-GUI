def format_file_size(bytesize: int):
    """
    Format the file size in bytes to a human-readable format.
    :param bytesize: The size of the file in bytes
    :return:
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffix_index = 0

    while bytesize >= 1024 and suffix_index < len(suffixes) - 1:
        bytesize /= 1024
        suffix_index += 1

    return f"{round(bytesize, 2)} {suffixes[suffix_index]}"
