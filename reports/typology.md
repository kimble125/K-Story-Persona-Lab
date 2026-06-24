# Persona Typology — auto report

- units: 4  | clusters (k): 2  | silhouette: 0.245

## Cluster signatures (features deviating most from the mean)

|   cluster |   n | members                                      | signature                                                                        |
|----------:|----:|:---------------------------------------------|:---------------------------------------------------------------------------------|
|         0 |   2 | 훈민정음, 임영                                     | n_sentences↑(+1.0), end_ni_ratio↑(+1.0), punct_ratio↓(-1.0), hangul_ratio↑(+1.0) |
|         1 |   2 | S1 (영화, 드라마, 전시회, 공연), S2 (영화, 드라마, 전시회, 공연) | n_sentences↓(-1.0), end_ni_ratio↓(-1.0), punct_ratio↑(+1.0), hangul_ratio↓(-1.0) |

## Per-unit features

| unit_id    | label                 | register   | period     |   n_sentences |   avg_sent_len |   std_sent_len |   avg_word_len |   ttr_word |   ttr_char |   hanja_ratio |   hangul_ratio |   punct_ratio |   hanja_sent_ratio |   end_da_ratio |   end_ra_ratio |   end_ni_ratio |   question_ratio |   honorific_ratio |   cluster |
|:-----------|:----------------------|:-----------|:-----------|--------------:|---------------:|---------------:|---------------:|-----------:|-----------:|--------------:|---------------:|--------------:|-------------------:|---------------:|---------------:|---------------:|-----------------:|------------------:|----------:|
| doc:훈민정음   | 훈민정음                  | literary   | historical |             6 |         19.333 |          5.821 |          2.762 |      1     |      0.664 |             0 |          1     |         0     |              0.143 |          0     |            0.5 |          0.167 |            0     |             0     |         0 |
| letter:임영  | 임영                    | letter     | historical |             6 |         13     |          1.826 |          2.786 |      0.964 |      0.705 |             0 |          1     |         0     |              0     |          0.333 |            0   |          0.167 |            0.167 |             0.167 |         0 |
| speaker:S1 | S1 (영화, 드라마, 전시회, 공연) | dialogue   | modern     |             2 |         18.5   |          3.5   |          2.643 |      1     |      0.784 |             0 |          0.892 |         0.108 |              0     |          0     |            0   |          0     |            0.5   |             0     |         1 |
| speaker:S2 | S2 (영화, 드라마, 전시회, 공연) | dialogue   | modern     |             2 |         15.5   |          1.5   |          2.385 |      1     |      0.871 |             0 |          0.871 |         0.129 |              0     |          0     |            0   |          0     |            0     |             0     |         1 |