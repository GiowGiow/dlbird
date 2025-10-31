# Dataset Download Setup Guide

## Prerequisites

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install kagglehub deeplake
# Only needed for BirdCLEF-2025 competition:
pip install kaggle
```

**Note:** The script now uses `kagglehub` for regular dataset downloads (recommended by Kaggle). The old `kaggle` API is only needed for competition downloads like BirdCLEF-2025.

### 2. Configure Kaggle API (Optional - only for BirdCLEF-2025)

If you want to download the BirdCLEF-2025 competition dataset, you need to configure Kaggle credentials:

1. Create a Kaggle account at [kaggle.com](https://www.kaggle.com)
2. Go to your Account settings
3. Scroll to "API" section and click "Create New API Token"
4. This downloads `kaggle.json` file
5. Move it to the correct location:

```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

**Note:** For regular dataset downloads (CUB-200, Xeno-Canto, 114 Species), kagglehub handles authentication automatically - no API key needed!

### 3. Accept Competition Rules (for BirdCLEF-2025)

Before downloading BirdCLEF-2025 dataset, you must:
1. Visit https://www.kaggle.com/competitions/birdclef-2025
2. Click "Join Competition" and accept the rules

## Usage

### Download All Datasets

```bash
python download_datasets.py --all
```

### Download Specific Datasets

**Image-based datasets:**
```bash
# CUB-200-2011
python download_datasets.py --cub200

# NABirds
python download_datasets.py --nabirds

# Both image datasets
python download_datasets.py --cub200 --nabirds
```

**Audio-based datasets:**
```bash
# Xeno-Canto bird recordings
python download_datasets.py --xeno-canto

# BirdCLEF-2025 competition
python download_datasets.py --birdclef2025

# Sound of 114 Species
python download_datasets.py --114species

# All audio datasets
python download_datasets.py --xeno-canto --birdclef2025 --114species
```

### Custom Output and Cache Directory

```bash
# Specify custom output directory for info files
python download_datasets.py --all --output /path/to/custom/datasets

# Set custom cache directory (where actual data is downloaded)
python download_datasets.py --all --cache /path/to/cache

# Or use environment variable
export KAGGLEHUB_CACHE=/path/to/cache
python download_datasets.py --all
```

## How kagglehub Works

**Important:** `kagglehub` downloads datasets to a cache directory (usually `~/.cache/kagglehub/`) and returns the path. This is the recommended approach as it:
- Avoids duplicate downloads across projects
- Manages versions automatically
- Saves disk space

### Customizing Cache Location

You can set where kagglehub downloads datasets using an environment variable:

```bash
# Set custom cache directory
export KAGGLEHUB_CACHE=/path/to/your/preferred/directory

# Then run the download script
python download_datasets.py --all
```

**For Google Colab users:** You must also disable Colab's cache for `KAGGLEHUB_CACHE` to work:

```python
import os
os.environ['DISABLE_COLAB_CACHE'] = "true"
os.environ['KAGGLEHUB_CACHE'] = "/content/datasets"
```

### Using Downloaded Data

The script will create `dataset_path.txt` files in each directory containing the actual location of the cached dataset. You can then:
- Use the cached path directly in your code
- Create symlinks: `ln -s <cached_path> datasets/image/cub200/data`
- Copy files if you need to modify them

## Dataset Structure

After downloading, your datasets will be organized as:

```
datasets/
├── image/
│   ├── cub200/           # CUB-200-2011 dataset (see dataset_path.txt for actual location)
│   └── nabirds/          # NABirds dataset info
└── audio/
    ├── xeno-canto/       # Xeno-Canto recordings (see dataset_path.txt for actual location)
    ├── birdclef2025/     # BirdCLEF-2025 competition data (downloaded directly here)
    └── 114species/       # 114 species audio dataset (see dataset_path.txt for actual location)
```

## Dataset Details

### CUB-200-2011
- **Type**: Image classification
- **Classes**: 200 bird species
- **Images**: ~12,000 images
- **Source**: Caltech-UCSD

### NABirds
- **Type**: Image classification
- **Classes**: 555 bird species
- **Images**: 48,000+ images
- **Note**: Accessed via deeplake streaming

### Xeno-Canto
- **Type**: Audio recordings
- **Coverage**: Species A-M (extended)
- **Format**: Audio files with metadata

### BirdCLEF-2025
- **Type**: Audio classification competition
- **Format**: Competition dataset with training/test splits
- **Note**: Requires competition acceptance

### Sound of 114 Species
- **Type**: Audio classification
- **Classes**: 114 bird species
- **Format**: Audio recordings

## Troubleshooting

### Kaggle API Errors

If you get authentication errors:
```bash
# Check if kaggle.json exists
ls -la ~/.kaggle/kaggle.json

# Verify permissions
chmod 600 ~/.kaggle/kaggle.json
```

### Competition Access Denied

For BirdCLEF-2025, make sure you:
1. Accepted the competition rules on Kaggle website
2. Are logged in with the same account as your API credentials

### Import Errors

If you get `ModuleNotFoundError`:
```bash
pip install --upgrade kaggle deeplake
```

### Disk Space

These datasets can be large. Ensure you have sufficient disk space:
- CUB-200-2011: ~1.2 GB
- NABirds: Streaming (minimal local storage)
- Xeno-Canto: ~15-20 GB
- BirdCLEF-2025: ~30-50 GB
- 114 Species: ~5-10 GB

Total recommended free space: **100+ GB**

## Help

For more options:
```bash
python download_datasets.py --help
```
