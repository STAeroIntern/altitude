from library import *

def run(data,folder_path):
# Define the allowed range for the difference
    for files in data:
            allowed_range = 100

            # List to store the split dataframes
            split_dfs = []
            start_idx = 0

            # Loop through the dataframe, checking the difference between consecutive rows
            for i in range(len(data[files]) - 1):
                current_value = data[files]['Mission Time'].iloc[i]
                next_value = data[files]['Mission Time'].iloc[i + 1]

                # Check if the difference is within the allowed range
                if abs(current_value - next_value) > allowed_range:
                    print(current_value,next_value)
                    # If the difference is larger than allowed, split the dataframe
                    split_dfs.append(data[files].iloc[start_idx:i + 1])
                    start_idx = i + 1

            # Append the last segment
            split_dfs.append(data[files].iloc[start_idx:])

            output_folder = os.path.join(folder_path, "split_csvs")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            #Split and export
            for index, split_df in enumerate(split_dfs):
                output_filename = os.path.join(output_folder, f"{files}_split_{index}.csv")
                split_df.to_csv(output_filename, index=False)
                print(f"Exported split CSV: {output_filename}")

    return output_folder
