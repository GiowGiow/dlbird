Image based

- CUB-200-2011 (Caltech-UCSD Birds 200)
    - https://www.kaggle.com/datasets/wenewone/cub2002011
- NABirds
    - https://datasets.activeloop.ai/docs/ml/datasets/nabirds-dataset/

Download NABirds Dataset in Python

import deeplake
ds = deeplake.load('hub://activeloop/nabirds-dataset-train')

Load NABirds Dataset Validation Subset in Python

import deeplake
ds = deeplake.load('hub://activeloop/nabirds-dataset-val')

============
Audio based
https://www.kaggle.com/datasets/rohanrao/xeno-canto-bird-recordings-extended-a-m

kaggle competitions download -c birdclef-2025
https://www.kaggle.com/datasets/rohanrao/xeno-canto-bird-recordings-extended-a-m
https://www.kaggle.com/datasets/soumendraprasad/sound-of-114-species-of-birds-till-2022?resource=download