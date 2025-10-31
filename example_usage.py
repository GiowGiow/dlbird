"""
Example: How to use downloaded datasets in your code

After running download_datasets.py, you can access the datasets using the
cached paths stored in dataset_path.txt files.
"""

from pathlib import Path


def get_dataset_path(dataset_name):
    """Read the cached dataset path from info file"""
    info_files = {
        "cub200": "datasets/image/cub200/dataset_path.txt",
        "xeno-canto": "datasets/audio/xeno-canto/dataset_path.txt",
        "114species": "datasets/audio/114species/dataset_path.txt",
        "birdclef2025": "datasets/audio/birdclef2025",  # Direct download
        "nabirds": "datasets/image/nabirds/dataset_info.txt",
    }

    info_path = Path(info_files[dataset_name])

    if not info_path.exists():
        raise FileNotFoundError(
            f"Dataset info file not found: {info_path}\n"
            f"Have you run download_datasets.py yet?"
        )

    # Read the first line which contains the path
    with open(info_path, "r") as f:
        first_line = f.readline().strip()
        if first_line.startswith("Dataset location:"):
            path_str = first_line.split("Dataset location:")[1].strip()
            return Path(path_str)

    return info_path.parent


# Example 1: Load CUB-200-2011 dataset
def load_cub200():
    """Example of loading CUB-200-2011 dataset"""
    dataset_path = get_dataset_path("cub200")
    print(f"CUB-200 dataset location: {dataset_path}")

    # List files in the dataset
    if dataset_path.exists():
        images_dir = dataset_path / "images"
        if images_dir.exists():
            print(f"Found {len(list(images_dir.rglob('*.jpg')))} images")

    return dataset_path


# Example 2: Load NABirds using deeplake
def load_nabirds():
    """Example of loading NABirds dataset via deeplake"""
    import deeplake

    # NABirds is accessed via streaming
    ds_train = deeplake.load("hub://activeloop/nabirds-dataset-train")
    ds_val = deeplake.load("hub://activeloop/nabirds-dataset-val")

    print(f"NABirds training samples: {len(ds_train)}")
    print(f"NABirds validation samples: {len(ds_val)}")

    return ds_train, ds_val


# Example 3: Load audio dataset
def load_audio_dataset(dataset_name="xeno-canto"):
    """Example of loading audio datasets"""
    dataset_path = get_dataset_path(dataset_name)
    print(f"{dataset_name} dataset location: {dataset_path}")

    # List audio files
    if dataset_path.exists():
        audio_files = (
            list(dataset_path.rglob("*.mp3"))
            + list(dataset_path.rglob("*.wav"))
            + list(dataset_path.rglob("*.ogg"))
        )
        print(f"Found {len(audio_files)} audio files")
        return audio_files

    return []


# Example 4: Using with PyTorch DataLoader
def create_pytorch_dataloader():
    """Example of creating a PyTorch DataLoader"""
    from torch.utils.data import Dataset, DataLoader
    from PIL import Image

    class BirdDataset(Dataset):
        def __init__(self, dataset_name="cub200", transform=None):
            self.dataset_path = get_dataset_path(dataset_name)
            self.transform = transform

            # Find all image files
            self.images = list(self.dataset_path.rglob("*.jpg")) + list(
                self.dataset_path.rglob("*.png")
            )

        def __len__(self):
            return len(self.images)

        def __getitem__(self, idx):
            img_path = self.images[idx]
            image = Image.open(img_path).convert("RGB")

            if self.transform:
                image = self.transform(image)

            # Extract label from path (this depends on dataset structure)
            label = img_path.parent.name

            return image, label

    # Create dataset and dataloader
    dataset = BirdDataset("cub200")
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

    return dataloader


if __name__ == "__main__":
    # Example usage
    print("Dataset Path Examples")
    print("=" * 60)

    try:
        cub_path = load_cub200()
        print()
    except FileNotFoundError as e:
        print(f"Error: {e}\n")

    try:
        audio_files = load_audio_dataset("xeno-canto")
        if audio_files:
            print(f"First audio file: {audio_files[0]}")
        print()
    except FileNotFoundError as e:
        print(f"Error: {e}\n")

    print("\nTo download datasets, run:")
    print("  python download_datasets.py --all")
