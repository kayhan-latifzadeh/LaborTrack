import numpy as np
import os
import shutil
import pandas as pd
import matplotlib.patches as mpatches
import argparse

import warnings
warnings.filterwarnings('ignore')

# Argument Parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Extract segmented timeseries from different modalities")
    parser.add_argument('--segments_info_file', type=str, default='data/segmentations_timestamps.csv', help="Path to the segments information CSV file.")
    parser.add_argument('--target_modality', type=str, required=True, choices=['pupil', 'fixations', 'saccades', 'blinks', 'head_movements'],
                        help="The target modality to process.")
    parser.add_argument('--target_participants_file', type=str, required=True, help="Path to the text file containing participant IDs.")
    return parser.parse_args()

# Load Participants from File
def load_participants(file_path):
    with open(file_path, 'r') as f:
        participants = [line.strip() for line in f.readlines()]
    return participants

def create_and_empty_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    print(f"Directory '{path}' created (or emptied if it already existed).")

def getIntervalDictionary(interval_info_filepath, participant_id, condition):
    interval_info_df = pd.read_csv(interval_info_filepath)
    interval_info_df = interval_info_df.sort_values(by='start_ts').reset_index(drop=True)
    df = interval_info_df[
        (interval_info_df['condition'] == condition) &
        (interval_info_df['participant_id'] == participant_id)
    ]
    interval_dict = df.groupby('segment_label').apply(lambda x: list(zip(x['start_ts'], x['end_ts']))).to_dict()
    return interval_dict

def main():
    args = parse_arguments()
    
    segments_info_file = args.segments_info_file
    target_modality = args.target_modality
    target_participants_file = args.target_participants_file

    # Load participants
    target_participants = load_participants(target_participants_file)
    participants = {'session_1': target_participants, 'session_2': target_participants}
    conditions = ['session_1', 'session_2']

    ANNOTATION_CODES = {'anamnesis': 0, 'vaginal examination': 1, 'awaiting': 2, 'preparation': 3, 'labor': 4}

    if target_modality == 'pupil':
        create_and_empty_dir('output/segmented_data/pupil/session_1')
        create_and_empty_dir('output/segmented_data/pupil/session_2')
        counter =  {'session_1':0, 'session_2':0}
        
        for condition in conditions:
            for participant_id in participants[condition]:
                pupil_data_path = f'data/pupil/{condition}/{participant_id}.csv'
                pupil_data_df = pd.read_csv(pupil_data_path)
                pupil_data_df = pupil_data_df[ (pupil_data_df['validity_left'] == 0) & (pupil_data_df['validity_right'] == 0)]
                pupil_data_df['left_right_pupil_avg'] = (pupil_data_df['pupil_left'] + pupil_data_df['pupil_right'])/2
                pupil_data_df['left_right_pupil_avg_normalized'] = (pupil_data_df['left_right_pupil_avg'] - pupil_data_df['left_right_pupil_avg'].min()) / (pupil_data_df['left_right_pupil_avg'].max() - pupil_data_df['left_right_pupil_avg'].min())
                interval_dict = getIntervalDictionary(segments_info_file, participant_id=participant_id, condition=condition)
                
                for segment_label, interval in interval_dict.items():
                    if len(interval) == 0:
                        continue
                    pupil_data_within_interval_df = pupil_data_df[ (pupil_data_df['timestamp'] >= interval[0][0]) & (pupil_data_df['timestamp'] < interval[0][1])]
                    pupil_data_within_interval_df = pupil_data_within_interval_df[['timestamp','x','y', 'left_right_pupil_avg_normalized']]
                    pupil_data_within_interval_df['interval_code'] = ANNOTATION_CODES[segment_label]
                    pupil_data_within_interval_df['timestamp'] = (pupil_data_within_interval_df['timestamp'] - interval[0][0])/(interval[0][1]-interval[0][0])
                    pupil_data_within_interval_df.to_csv(f'output/segmented_data/pupil/{condition}/{counter[condition]}.csv', index=False)
                    counter[condition] += 1
        print('Data available at: output/segmented_data/pupil/')            

    elif target_modality == 'fixations':
        counter =  {'session_1':0, 'session_2':0}
        create_and_empty_dir('output/segmented_data/fixations/session_1')
        create_and_empty_dir('output/segmented_data/fixations/session_2')

        for condition in conditions:
            for participant_id in participants[condition]:
                fixation_data_path = f'data/fixations/{condition}/{participant_id}.csv'
                fixation_data_df = pd.read_csv(fixation_data_path)
                interval_dict = getIntervalDictionary(segments_info_file, participant_id=participant_id, condition=condition)
                
                for segment_label, interval in interval_dict.items():
                    if len(interval) == 0:
                        continue
                    fixation_data_within_interval_df = fixation_data_df[ (fixation_data_df['timestamp'] >= interval[0][0]) & (fixation_data_df['timestamp'] < interval[0][1])]
                    fixation_data_within_interval_df['timestamp'] =  (fixation_data_within_interval_df['timestamp'] - interval[0][0])/(interval[0][1]-interval[0][0])
                    fixation_data_within_interval_df = fixation_data_within_interval_df[['timestamp','x','y','duration']]
                    fixation_data_within_interval_df['interval_code'] = ANNOTATION_CODES[segment_label]
                    fixation_data_within_interval_df.to_csv(f'output/segmented_data/fixations/{condition}/{counter[condition]}.csv', index=False)
                    counter[condition] += 1
        print('Data available at: output/segmented_data/fixations/')

    elif target_modality == 'saccades':
        counter =  {'session_1':0, 'session_2':0}
        create_and_empty_dir('output/segmented_data/saccades/session_1')
        create_and_empty_dir('output/segmented_data/saccades/session_2')

        for condition in conditions:
            for participant_id in participants[condition]:
                interval_dict = getIntervalDictionary(segments_info_file, participant_id=participant_id, condition=condition)
                for segment_label, interval in interval_dict.items():
                    if len(interval) == 0:
                        continue
                    saccade_data_path = f'data/saccades/{condition}/{participant_id}.csv'
                    saccade_data_df = pd.read_csv(saccade_data_path)
                    saccade_data_within_interval_df = saccade_data_df[ (saccade_data_df['start'] >= interval[0][0]) &
                                                                    (saccade_data_df['start'] < interval[0][1]) &
                                                                    (saccade_data_df['end'] >= interval[0][0]) &
                                                                    (saccade_data_df['end'] < interval[0][1])]
                    saccade_data_within_interval_df['start'] =  (saccade_data_within_interval_df['start'] - interval[0][0])/(interval[0][1]-interval[0][0])
                    saccade_data_within_interval_df['end'] =  (saccade_data_within_interval_df['end'] - interval[0][0])/(interval[0][1]-interval[0][0])
                    saccade_data_within_interval_df['interval_code'] = ANNOTATION_CODES[segment_label]
                    saccade_data_within_interval_df.to_csv(f'output/segmented_data/saccades/{condition}/{counter[condition]}.csv', index=False)
                    counter[condition] += 1
        print('Data available at: output/segmented_data/saccades/')

    elif target_modality == 'blinks':
        counter =  {'session_1':0, 'session_2':0}
        create_and_empty_dir('output/segmented_data/blinks/session_1')
        create_and_empty_dir('output/segmented_data/blinks/session_2')

        for condition in conditions:
            for participant_id in participants[condition]:
                blink_data_path = f'data/blinks/{condition}/{participant_id}.csv'
                if not os.path.exists(blink_data_path):
                    continue
                blink_data_df = pd.read_csv(blink_data_path)

                interval_dict = getIntervalDictionary(segments_info_file, participant_id=participant_id, condition=condition)
                for segment_label, interval in interval_dict.items():
                    if len(interval) == 0:
                        continue
                    blink_data_within_interval_df = blink_data_df[ (blink_data_df['start'] >= interval[0][0])
                                                                  & (blink_data_df['start'] < interval[0][1])]
                    blink_data_within_interval_df['start'] =  (blink_data_within_interval_df['start'] - interval[0][0])/(interval[0][1]-interval[0][0])
                    blink_data_within_interval_df['interval_code'] = ANNOTATION_CODES[segment_label]
                    blink_data_within_interval_df.to_csv(f'output/segmented_data/blinks/{condition}/{counter[condition]}.csv', index=False)
                    counter[condition] += 1
        print('Data available at: output/segmented_data/blinks/')

    elif target_modality == 'head_movements':
        counter =  {'session_1':0, 'session_2':0}
        create_and_empty_dir('output/segmented_data/head-movements/session_1')
        create_and_empty_dir('output/segmented_data/head-movements/session_2')

        for condition in conditions:
            for participant_id in participants[condition]:
                interval_dict = getIntervalDictionary(segments_info_file, participant_id=participant_id, condition=condition)
                for segment_label, interval in interval_dict.items():
                    if len(interval) == 0:
                        continue
                    head_data_path = f'data/head-movements/{condition}/{participant_id}.csv'
                    head_data_df = pd.read_csv(head_data_path)
                    head_data_within_interval_df = head_data_df[ (head_data_df['timestamp'] >= interval[0][0]) &
                                                                (head_data_df['timestamp'] < interval[0][1])]
                    head_data_within_interval_df['timestamp'] =  (head_data_within_interval_df['timestamp'] - interval[0][0])/(interval[0][1]-interval[0][0])
                    head_data_within_interval_df['interval_code'] = ANNOTATION_CODES[segment_label]
                    head_data_within_interval_df.to_csv(f'output/segmented_data/head-movements/{condition}/{counter[condition]}.csv', index=False)
                    counter[condition] += 1
        print('Data available at: output/segmented_data/head-movements/')

if __name__ == "__main__":
    main()
