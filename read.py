from library import *
import func

def run(parent_path, _filter_func):
    #Create two empty library to store the data and file size
    data_lib = {}
    sizes = {}

    for file in os.listdir(parent_path):
        file_path = os.path.join(parent_path, file)
        files_size = os.path.getsize(file_path)
        if ((files_size >= 400845463) | (files_size <= 321410)): #Remove files that are above or equal to this byte size
            os.remove(file_path)

        trim_name = file[0:15]
        #pool = Pool(8) #
        try:
            #data = pool.map(func.reader, file_path)
            data = pd.read_csv(file_path)
            filtered_data = _filter_func(data)  # Call the filter function
            if isinstance(filtered_data, pd.DataFrame):
                data_lib[trim_name] = filtered_data
                sizes[trim_name] = os.path.getsize(file_path)
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

    # Remove smaller files with similar names
    keys = list(sizes.keys())
    keys_to_remove = []

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            filename1, filename2 = keys[i], keys[j]
            if func.compare(filename1, filename2):
                # Compare file sizes and add the smaller one to removal list
                keys_to_remove.append(filename1 if sizes[filename1] < sizes[filename2] else filename2)
                break

    for key in keys_to_remove:
        data_lib.pop(key, None)
        sizes.pop(key, None)  

    return data_lib