# LaborTrack

**Note:** This repository provides only 5 randomly selected data samples, for the UMAP reviewers, which include all the corresponding data (fixations, pupil data, saccades, blinks, and head movements). We will publish the full dataset upon paper acceptance.


## Data Description

### Video recordings

In `data/video-recordings` you can find screen recordings for each participants.

Example (trimmed from the full video, converted to a GIF):

![Recording Example](video-example.gif)

### Skill scores
The (comma-delimited) skill score file `data/skill-scores.csv` has 3 columns:

  - `participant_id`: (string) Participant ID
  - `session_1_score`: (float) The skill score of the first session
  - `session_2_score`: (float) The skill score of the second session

    Example:
    ```csv
    participant_id,session_1_score,session_2_score
    3ShqB,3.1,3.3
    4rE3i,2.4,3.5
    ...
    ```

Each data eye/head movement data directory (`data/pupil`, `data/fixations`, `data/saccades`, `data/blinks`, `data/head-movements`) contains two subfolders, `session_1` and `session_2`. To find a participant's data, look for the `[participant_id].csv`. For example, if you are looking for the pupil data of participant `3ShqB` in session 2, the file would be located at `data/pupil/session_2/3ShqB.csv`.


### Pupil
The (comma-delimited) pupil dilation files in `data/pupil` has 7 columns:

  - `timestamp`: (int) Unix timestamp in milliseconds
  - `x`: (int) Gaze data X-coordinate (relative to top-left corner of the screen), average of the X-coordinates of the left and right eye, in pixels
  - `y`: (int) Gaze data Y-coordinate (relative to top-left corner of the screen), average of the Y-coordinates of the left and right eye, in pixels
  - `pupil_left`: (int) Pupil diameter of the left eye in millimeter
  - `pupil_right`: (int) Pupil diameter of the right eye in millimeter
  - `validity_left`: (int) Level of certainty that eye-tracker has recorded valid data for the left eye (0 = certainly valid, 5 = certainly invalid)
  - `validity_right`: (int) Level of certainty that eye-tracker has recorded valid data for the right eye (0 = certainly valid, 5 = certainly invalid)

    Example:
    ```csv
    timestamp,x,y,pupil_left,pupil_right,validity_left,validity_right
    1621930481582,1004,304,3,4,0,0
    ...
    ```

### Fixations
The (comma-delimited) fixation data files in `data/fixations` has 4 columns:

  - `timestamp`: (int) Unix timestamp indicating when the fixation happens in milliseconds
  - `x`: (int) X-coordinate of the fixation centroid (relative to top-left corner of the screen) in pixels
  - `y`: (int) Y-coordinate of the fixation centroid (relative to top-left corner of the screen) in pixels
  - `duration`: (int) Duration of the fixation in milliseconds

    Example:
    ```csv
    timestamp,x,y,duration
    1621930481587,1001,301,690
    ...
    ```

### Saccades
The (comma-delimited) saccade data files in `data/saccades` has 8 columns:

  - `start`: (int) Unix timestamp in milliseconds indicating when the saccade starts
  - `end`: (int) Unix timestamp in milliseconds indicating when the saccade ends
  - `duration`: (int) The duration of the saccade in milliseconds
  - `amplitude`: (int) Amplitude of the saccade in degrees
  - `peak_velocity`: (int) Peak velocity of the saccade in degrees per second
  - `peak_acceleration`: (float) Peak acceleration of the saccade in degrees per second squared
  - `peak_deceleration`: (int) Peak deceleration of the saccade in degrees per second squared
  - `direction`: (int) Direction of the saccade from its start point to end point in from top to bottom in degrees

    Example:
    ```csv
    start,end,duration,amplitude,peak_velocity,peak_acceleration,peak_deceleration,direction
    1621930482277,1621930482297,20,0,46,2432.36186889215,-1,264
    ...
    ```

### Blinks
The (comma-delimited) blink data files in `data/blinks` has 3 columns:

  - `start`: (int) Unix timestamp in milliseconds indicating when the blink starts
  - `end`: (int) Unix timestamp in milliseconds indicating when the blink ends
  - `duration`: (int) The duration of the blink in milliseconds
    
    Example:
    ```csv
    start,end,duration
    1621930481812,1621930481822,10
    ...
    ```
### Head movements
The (comma-delimited) head movement data files in `data/head-movements` has 7 columns:

  - `timestamp`: (int) Unix timestamp in milliseconds
  - `gyro_x`: (float) Rotation of the glasses along the X-axis in degrees per second
  - `gyro_y`: (float) Rotation of the glasses along the Y-axis in degrees per second
  - `gyro_z`: (float) Rotation of the glasses along the Z-axis in degrees per second
  - `acc_x`: (float) Motion along the X-axis in millimeter per second squared
  - `acc_y`: (float) Motion along the Y-axis in millimeter per second squared
  - `acc_z`: (float) Motion along the Z-axis in millimeter per second squared

    Example:
    ```csv
    timestamp,gyro_x,gyro_y,gyro_z,acc_x,acc_y,acc_z
    1621588449221,0.0,0.0,0.0,0.0,0.0,0.0
    1621588449230,-1.190000057220459,4.4679999351501465,-5.183000087738037,-0.0780000016093254,-9.791999816894531,-1.1690000295639038
    ...
    ```

### Segmentation data

The (comma-delimited) segmentation information data `data/segmentations_timestamps.csv` has 5 columns:

  - `participant_id`: (int) (string) Participant ID
  - `condition`: (string) The session number ['session_1', 'session_2']
  - `segment_label`: (string) The label of the segment ['anamnesis', 'vaginal examination', 'preparation', 'awaiting', 'labor']
  - `start_ts`: (int) Unix timestamp in milliseconds indicating when the segment starts
  - `end_ts`: (int) Unix timestamp in milliseconds indicating when the segment starts

    Example:
    ```csv
    participant_id,condition,annotation_label,start_ts,end_ts
    3ShqB,session_1,anamnesis,1621586562309,1621586618625
    ...
    ```
## Scripts

### How to segment time series with normalized timestamps?

You can extract the timeseries within each segment (e.g., labor, anamnesis) for each modality and for a list of participants. For example, the command below extracts head movement time series:

```shell
python prepare_timeseries.py --target_modality head_movements --target_participants_file target_participants.txt
```

The output will be a number of CSV files separated into two folders: session_1 and session_2.

Example:
```csv
timestamp,gyro_x,gyro_y,gyro_z,acc_x,acc_y,acc_z,interval_code
0.0,-35.209999084472656,-31.66900062561035,-28.400999069213867,2.000999927520752,-8.270999908447266,0.3740000128746032,0
...
0.9996110109824566,-23.100000381469727,-8.996999740600586,9.501999855041506,-0.1180000007152557,-8.67300033569336,4.684000015258789,0
...
```

The output files contain normalized timestamps relative to the start of the segment, and they also contain the segment code (as `interval_code`) with this mapping:

```python
{'anamnesis': 0, 'vaginal examination': 1, 'awaiting': 2, 'preparation': 3, 'labor': 4}
```

These files can be used for different purposes, such as training RNN models, extracting features, or creating plots and visualizations.


### How to extract handcrafted features?

After having the time series with normalized timestamps. You can run each of the `calculate_handcrafted_features_[MODALITY].py` scripts to extract handcrafted features.

Example:
```shell
python3 calculate_handcrafted_features_pupil.py --chunk_size 100 --target_segment 'vaginal examination'
```

In this example, the script processes `100` successive timesteps to extract features from the pupil data within the `vaginal examination` segment. It generates two files:

  - `X_pupil.npy`: The feature set
  - `y_pupil.npy`: The labels (binary: `0` for the first session and `1` for the second session)

These files can later be loaded for any classification task (e.g., using SVM, XGBoost) on the handcrafted features.
