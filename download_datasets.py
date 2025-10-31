#!/usr/bin/env python3
"""
Dataset Download Script for Bird Classification Project

This script downloads various bird datasets including:
- CUB-200-2011 (image-based)
- NABirds (image-based)
- Xeno-Canto bird recordings (audio-based)
- BirdCLEF-2025 (audio-based)
- Sound of 114 species dataset (audio-based)

Requirements:
- kagglehub library installed
- deeplake library installed
- Kaggle API credentials configured (~/.kaggle/kaggle.json) for competition downloads

Environment Variables:
- KAGGLEHUB_CACHE: Set custom cache directory for kagglehub downloads
  Example: export KAGGLEHUB_CACHE=/path/to/datasets
- DISABLE_COLAB_CACHE: Set to "true" in Google Colab for KAGGLEHUB_CACHE to work
  Example: export DISABLE_COLAB_CACHE=true
"""

import sys
import os
import argparse
import shutil
from pathlib import Path


def setup_directories(base_path):
    """Create necessary directories for datasets"""
    datasets_dir = Path(base_path)

    # Create subdirectories
    (datasets_dir / "image" / "cub200").mkdir(parents=True, exist_ok=True)
    (datasets_dir / "image" / "nabirds").mkdir(parents=True, exist_ok=True)
    (datasets_dir / "audio" / "xeno-canto").mkdir(parents=True, exist_ok=True)
    (datasets_dir / "audio" / "birdclef2025").mkdir(parents=True, exist_ok=True)
    (datasets_dir / "audio" / "114species").mkdir(parents=True, exist_ok=True)

    return datasets_dir


def download_cub200(datasets_dir):
    """Download CUB-200-2011 dataset from Kaggle"""
    print("\n" + "=" * 60)
    print("Downloading CUB-200-2011 Dataset")
    print("=" * 60)

    try:
        import kagglehub

        output_dir = datasets_dir / "image" / "cub200"

        print(f"Downloading to: {output_dir}")
        # Download using kagglehub (downloads to cache, then we can copy/symlink)
        path = kagglehub.dataset_download("wenewone/cub2002011")
        print(f"Dataset downloaded to: {path}")
        print(f"Note: Dataset cached at {path}")
        print(f"To use in your project, copy or symlink to: {output_dir}")

        # Create a symlink or info file
        info_file = output_dir / "dataset_path.txt"
        with open(info_file, "w") as f:
            f.write(f"Dataset location: {path}\n")
            f.write(f"Dataset: wenewone/cub2002011\n")

        print("✓ CUB-200-2011 downloaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error downloading CUB-200-2011: {e}")
        return False


def download_nabirds(datasets_dir):
    """Download NABirds dataset using deeplake"""
    print("\n" + "=" * 60)
    print("Downloading NABirds Dataset")
    print("=" * 60)

    try:
        import deeplake

        output_dir = datasets_dir / "image" / "nabirds"

        print("Downloading NABirds training set...")
        ds_train = deeplake.load("hub://activeloop/nabirds-dataset-train")
        print(f"Training set loaded: {len(ds_train)} samples")

        print("Downloading NABirds validation set...")
        ds_val = deeplake.load("hub://activeloop/nabirds-dataset-val")
        print(f"Validation set loaded: {len(ds_val)} samples")

        # Save dataset paths to a file for reference
        info_file = output_dir / "dataset_info.txt"
        with open(info_file, "w") as f:
            f.write("NABirds Dataset Information\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Training set: hub://activeloop/nabirds-dataset-train\n")
            f.write(f"Training samples: {len(ds_train)}\n\n")
            f.write(f"Validation set: hub://activeloop/nabirds-dataset-val\n")
            f.write(f"Validation samples: {len(ds_val)}\n\n")
            f.write("Note: This dataset is accessed via deeplake streaming.\n")
            f.write(
                "To use: ds = deeplake.load('hub://activeloop/nabirds-dataset-train')\n"
            )

        print(f"✓ NABirds dataset info saved to: {info_file}")
        print("Note: NABirds uses streaming from deeplake hub")
        return True
    except Exception as e:
        print(f"✗ Error loading NABirds: {e}")
        return False


def download_xeno_canto(datasets_dir):
    """Download Xeno-Canto bird recordings from Kaggle"""
    print("\n" + "=" * 60)
    print("Downloading Xeno-Canto Bird Recordings")
    print("=" * 60)

    try:
        import kagglehub

        output_dir = datasets_dir / "audio" / "xeno-canto"

        print(f"Downloading to: {output_dir}")
        # Download using kagglehub
        path = kagglehub.dataset_download(
            "rohanrao/xeno-canto-bird-recordings-extended-a-m"
        )
        print(f"Dataset downloaded to: {path}")
        print(f"Note: Dataset cached at {path}")
        print(f"To use in your project, copy or symlink to: {output_dir}")

        # Create a info file
        info_file = output_dir / "dataset_path.txt"
        with open(info_file, "w") as f:
            f.write(f"Dataset location: {path}\n")
            f.write("Dataset: rohanrao/xeno-canto-bird-recordings-extended-a-m\n")

        print("✓ Xeno-Canto dataset downloaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error downloading Xeno-Canto: {e}")
        return False


def download_birdclef2025(datasets_dir):
    """Download BirdCLEF-2025 competition data from Kaggle

    Note: Competition downloads still use the kaggle API as kagglehub
    doesn't support competition downloads yet.
    """
    print("\n" + "=" * 60)
    print("Downloading BirdCLEF-2025 Competition Data")
    print("=" * 60)

    try:
        import kaggle

        output_dir = datasets_dir / "audio" / "birdclef2025"

        print(f"Downloading to: {output_dir}")
        print("Note: You must accept competition rules on Kaggle website first!")
        kaggle.api.competition_download_files(
            "birdclef-2025", path=str(output_dir), quiet=False
        )
        print("Extracting files...")
        import zipfile

        for zip_file in output_dir.glob("*.zip"):
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(output_dir)
            print(f"Extracted: {zip_file.name}")

        print("✓ BirdCLEF-2025 downloaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error downloading BirdCLEF-2025: {e}")
        print("Note: Make sure you've accepted the competition rules on Kaggle")
        return False


def download_114species(datasets_dir):
    """Download Sound of 114 Species dataset from Kaggle"""
    print("\n" + "=" * 60)
    print("Downloading Sound of 114 Species Dataset")
    print("=" * 60)

    try:
        import kagglehub

        output_dir = datasets_dir / "audio" / "114species"

        print(f"Downloading to: {output_dir}")
        # Download using kagglehub
        path = kagglehub.dataset_download(
            "soumendraprasad/sound-of-114-species-of-birds-till-2022"
        )
        print(f"Dataset downloaded to: {path}")
        print(f"Note: Dataset cached at {path}")
        print(f"To use in your project, copy or symlink to: {output_dir}")

        # Create a info file
        info_file = output_dir / "dataset_path.txt"
        with open(info_file, "w") as f:
            f.write(f"Dataset location: {path}\n")
            f.write(
                "Dataset: soumendraprasad/sound-of-114-species-of-birds-till-2022\n"
            )

        print("✓ Sound of 114 Species downloaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error downloading 114 Species dataset: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download bird classification datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all datasets
  python download_datasets.py --all
  
  # Download only image-based datasets
  python download_datasets.py --cub200 --nabirds
  
  # Download only audio-based datasets
  python download_datasets.py --xeno-canto --birdclef2025 --114species
  
  # Download specific datasets
  python download_datasets.py --cub200 --birdclef2025
  
  # Specify custom output directory
  python download_datasets.py --all --output /path/to/datasets
  
  # Set custom cache directory for kagglehub
  python download_datasets.py --all --cache /path/to/cache
  
  # Or use environment variable
  export KAGGLEHUB_CACHE=/path/to/cache
  python download_datasets.py --all

Environment Variables:
  KAGGLEHUB_CACHE         Set custom cache directory for downloads
  DISABLE_COLAB_CACHE     Set to "true" in Google Colab for KAGGLEHUB_CACHE to work
        """,
    )

    parser.add_argument("--all", action="store_true", help="Download all datasets")
    parser.add_argument(
        "--cub200", action="store_true", help="Download CUB-200-2011 dataset"
    )
    parser.add_argument(
        "--nabirds", action="store_true", help="Download NABirds dataset"
    )
    parser.add_argument(
        "--xeno-canto", action="store_true", help="Download Xeno-Canto bird recordings"
    )
    parser.add_argument(
        "--birdclef2025",
        action="store_true",
        help="Download BirdCLEF-2025 competition data",
    )
    parser.add_argument(
        "--114species",
        action="store_true",
        help="Download Sound of 114 Species dataset",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./datasets",
        help="Output directory for datasets (default: ./datasets)",
    )
    parser.add_argument(
        "--cache",
        type=str,
        help="Set kagglehub cache directory (alternative to KAGGLEHUB_CACHE env var)",
    )

    args = parser.parse_args()

    # Set cache directory if provided via command line
    if args.cache:
        os.environ["KAGGLEHUB_CACHE"] = args.cache
        print(f"Setting KAGGLEHUB_CACHE to: {args.cache}\n")

    # If no specific dataset is selected and --all is not set, show help
    if not any(
        [
            args.all,
            args.cub200,
            args.nabirds,
            args.xeno_canto,
            args.birdclef2025,
            args.__dict__["114species"],
        ]
    ):
        parser.print_help()
        sys.exit(1)

    # Display cache directory information
    print("=" * 60)
    print("Environment Configuration")
    print("=" * 60)

    kagglehub_cache = os.environ.get("KAGGLEHUB_CACHE")
    if kagglehub_cache:
        print(f"✓ KAGGLEHUB_CACHE set to: {kagglehub_cache}")
    else:
        default_cache = os.path.expanduser("~/.cache/kagglehub")
        print(f"ℹ KAGGLEHUB_CACHE not set, using default: {default_cache}")
        print("  To change, run: export KAGGLEHUB_CACHE=/your/path")

    # Check for Google Colab
    try:
        import google.colab

        disable_colab = os.environ.get("DISABLE_COLAB_CACHE")
        if disable_colab == "true":
            print("✓ DISABLE_COLAB_CACHE is set (Google Colab detected)")
        else:
            print("⚠ Google Colab detected! For KAGGLEHUB_CACHE to work, run:")
            print("  os.environ['DISABLE_COLAB_CACHE'] = 'true'")
    except ImportError:
        pass  # Not in Colab

    print()

    # Check for required packages
    print("Checking required packages...")
    missing_packages = []

    try:
        import kagglehub

        print("✓ kagglehub package found")
    except ImportError:
        print("✗ kagglehub package not found")
        missing_packages.append("kagglehub")

    # Only check for kaggle if downloading competitions
    if args.all or args.birdclef2025:
        try:
            import kaggle

            print("✓ kaggle package found (needed for competitions)")
        except ImportError:
            print("✗ kaggle package not found (needed for BirdCLEF-2025)")
            missing_packages.append("kaggle")

    try:
        import deeplake

        print("✓ deeplake package found")
    except ImportError:
        print("✗ deeplake package not found")
        missing_packages.append("deeplake")

    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
        print(
            "\nNote: Kaggle API credentials are only needed for competition downloads (BirdCLEF-2025):"
        )
        print("  1. Create account on kaggle.com")
        print("  2. Go to Account settings -> API -> Create New API Token")
        print("  3. Save kaggle.json to ~/.kaggle/kaggle.json")
        print("  4. chmod 600 ~/.kaggle/kaggle.json")
        sys.exit(1)

    # Setup directories
    datasets_dir = setup_directories(args.output)
    print(f"\nDatasets will be saved to: {datasets_dir.absolute()}")

    # Track results
    results = {}

    # Download selected datasets
    if args.all or args.cub200:
        results["CUB-200-2011"] = download_cub200(datasets_dir)

    if args.all or args.nabirds:
        results["NABirds"] = download_nabirds(datasets_dir)

    if args.all or args.xeno_canto:
        results["Xeno-Canto"] = download_xeno_canto(datasets_dir)

    if args.all or args.birdclef2025:
        results["BirdCLEF-2025"] = download_birdclef2025(datasets_dir)

    if args.all or args.__dict__["114species"]:
        results["114 Species"] = download_114species(datasets_dir)

    # Print summary
    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    for dataset, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        print(f"{dataset}: {status}")

    successful = sum(results.values())
    total = len(results)
    print(f"\nTotal: {successful}/{total} datasets downloaded successfully")

    if successful < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
