# DLBird - Deep Learning for Bird Classification

A project for bird species classification using deep learning on image and audio datasets.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Datasets

```bash
# Download all datasets
python download_datasets.py --all

# Or download specific datasets
python download_datasets.py --cub200 --nabirds  # Image datasets
python download_datasets.py --xeno-canto --birdclef2025  # Audio datasets

# Set custom cache directory
python download_datasets.py --all --cache /path/to/datasets
```

For detailed setup instructions, see [DATASET_SETUP.md](DATASET_SETUP.md).

### 3. Use the Datasets

See [example_usage.py](example_usage.py) for examples of loading and using the datasets in your code.

## Available Datasets

### Image-Based Datasets

#### CUB-200-2011 (Caltech-UCSD Birds 200)
- **Classes**: 200 bird species
- **Images**: ~12,000 images
- **Size**: ~1.2 GB
- **Source**: [Kaggle](https://www.kaggle.com/datasets/wenewone/cub2002011)

#### NABirds
- **Classes**: 555 bird species  
- **Images**: 48,000+ images
- **Access**: Streaming via deeplake
- **Source**: [ActiveLoop](https://datasets.activeloop.ai/docs/ml/datasets/nabirds-dataset/)

```python
import deeplake
ds_train = deeplake.load('hub://activeloop/nabirds-dataset-train')
ds_val = deeplake.load('hub://activeloop/nabirds-dataset-val')
```

### Audio-Based Datasets

#### Xeno-Canto Bird Recordings (Extended A-M)
- **Coverage**: Bird species A-M
- **Size**: ~15-20 GB
- **Source**: [Kaggle](https://www.kaggle.com/datasets/rohanrao/xeno-canto-bird-recordings-extended-a-m)

#### BirdCLEF-2025
- **Type**: Competition dataset
- **Size**: ~30-50 GB
- **Note**: Requires accepting competition rules
- **Source**: [Kaggle Competition](https://www.kaggle.com/competitions/birdclef-2025)

#### Sound of 114 Species of Birds
- **Classes**: 114 bird species
- **Size**: ~5-10 GB
- **Source**: [Kaggle](https://www.kaggle.com/datasets/soumendraprasad/sound-of-114-species-of-birds-till-2022)

## Project Structure

```
dlbird/
├── README.md                   # This file
├── DATASET_SETUP.md           # Detailed dataset setup guide
├── requirements.txt           # Python dependencies
├── download_datasets.py       # Dataset download script
├── example_usage.py          # Example code for using datasets
├── datasets/                 # Downloaded datasets (created after download)
│   ├── image/
│   │   ├── cub200/
│   │   └── nabirds/
│   └── audio/
│       ├── xeno-canto/
│       ├── birdclef2025/
│       └── 114species/
├── experiments/              # Experiment results and logs
└── src/                      # Source code
```

## Environment Variables

- **`KAGGLEHUB_CACHE`**: Set custom cache directory for kagglehub downloads
  ```bash
  export KAGGLEHUB_CACHE=/path/to/your/datasets
  ```

- **`DISABLE_COLAB_CACHE`**: Required in Google Colab for `KAGGLEHUB_CACHE` to work
  ```python
  import os
  os.environ['DISABLE_COLAB_CACHE'] = "true"
  os.environ['KAGGLEHUB_CACHE'] = "/content/datasets"
  ```

## Requirements

- Python 3.8+
- kagglehub >= 0.2.0
- deeplake >= 3.8.0
- kaggle >= 1.5.16 (only for BirdCLEF-2025 competition)

## Troubleshooting

See [DATASET_SETUP.md](DATASET_SETUP.md) for detailed troubleshooting steps, including:
- Kaggle API configuration
- Competition access setup
- Disk space requirements
- Common error solutions

## License

This project uses publicly available datasets. Please refer to each dataset's original license:
- CUB-200-2011: [Original source](http://www.vision.caltech.edu/datasets/cub_200_2011/)
- NABirds: [Dataset info](https://dl.allaboutbirds.org/nabirds)
- Xeno-Canto: [Terms of use](https://xeno-canto.org/about/terms)
- BirdCLEF-2025: Kaggle competition rules apply