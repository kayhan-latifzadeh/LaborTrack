import os
import pandas as pd
import numpy as np
import argparse

def load_csv_files(directory):
    file_data = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            filepath = os.path.join(directory, file)
            data = pd.read_csv(filepath)
            if len(data) == 0:
                continue
            file_data.append(data)
    return file_data


def extract_features(data_list, class_label, target_interval_codes, chunk_size):
    processed_data = []
    processed_labels = []

    for data in data_list:
        interval_code = data.iloc[0]['interval_code']
        timestamps = data[['timestamp']]
        data = data[['x','y', 'left_right_pupil_avg_normalized']]
        
        if not interval_code in target_interval_codes:
            continue
        
        for i in range(0, len(data), chunk_size):
            chunk = data.iloc[i:i+chunk_size]
            ts_chunk = timestamps.iloc[i:i+chunk_size]
            start = ts_chunk.iloc[0]['timestamp']
            end = ts_chunk.iloc[-1]['timestamp']
            if len(chunk) < chunk_size:
                # Zero pad if the chunk is smaller than chunk_size
                padding = pd.DataFrame(np.zeros((chunk_size - len(chunk), len(chunk.columns))), columns=chunk.columns)
                chunk = pd.concat([chunk, padding], ignore_index=True)
            
            # Calculate summary statistics for the chunk
            mean_values = chunk.mean().values
            std_values = chunk.std().values
            median_values = chunk.median().values
            min_values = chunk.min().values
            max_values = chunk.max().values
            
            
            # Flatten the statistics into a single array
            summary_stats = np.concatenate([mean_values, std_values, median_values, min_values, max_values, [start],[end], [interval_code]])
            
            
            processed_data.append(summary_stats)  # Summary statistics as a feature vector
            processed_labels.append(class_label)

    return processed_data, processed_labels


def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract handcrafted features from pupil data.')
    parser.add_argument('--chunk_size', type=int, default=100, help='Size of chunks (timestep) for feature extraction (default: 100)')
    parser.add_argument('--target_segment', type=str, default='ALL', choices=['anamnesis', 'vaginal examination', 'awaiting', 'preparation', 'labor', 'ALL'], help='Target interval for data (default: ALL)')
    return parser.parse_args()


def main():
    args = parse_arguments()

    chunk_size = args.chunk_size
    target_interval = args.target_segment

    ANNOTATION_CODES = {'anamnesis': 0, 'vaginal examination': 1, 'awaiting': 2, 'preparation': 3, 'labor': 4 }

    target_interval_codes = [0, 1, 2, 3, 4] if target_interval == 'ALL' else [ANNOTATION_CODES[target_interval]]

    session_1_data = load_csv_files('output/segmented_data/pupil/session_1')
    session_2_data = load_csv_files('output/segmented_data/pupil/session_2')

    session_1_processed_data, session_1_labels = extract_features(session_1_data, class_label=0, target_interval_codes=target_interval_codes, chunk_size=chunk_size)
    session_2_processed_data, session_2_labels = extract_features(session_2_data, class_label=1, target_interval_codes=target_interval_codes, chunk_size=chunk_size)

    X = np.array(session_1_processed_data + session_2_processed_data)
    y = np.array(session_1_labels + session_2_labels)

    np.save('output/X_pupil.npy', X)
    np.save('output/X_pupil.npy', y)
    
    print('X: output/X_pupil.npy')
    print('y: output/y_pupil.npy')


if __name__ == '__main__':
    main()