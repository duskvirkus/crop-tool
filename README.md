# Crop Tool

A utility for quickly cropping large collections of images.

Inspired by Derrick Schultz's [dataset-tools](https://github.com/dvschultz/dataset-tools).

## Setup

It's suggested that you use Anaconda. Download at: [https://www.anaconda.com/products/individual#Downloads](https://www.anaconda.com/products/individual#Downloads).

```bash
conda create -n crop-tool python=3.8 # note 3.9 doesn't seem to work
conda activate
pip install -r requirements.txt
```

## Using

Example

```
python run.py --input_directories "/path/to/images /another/optional/directory" --save_directory "/path/to/save/directory"
```

Use 'd' to go forward and 'a' to go backwards. Once you've reached the end of the list press 'esc' to exit and wait for program to close (this ensures all edits are saved properly).


# Still TODO

Pull requests are welcome.

- [ ] change hard coded padding
- [ ] Fix file list selection
- [ ] Fix off by one crops
- [ ] Display previous crops
- [ ] Undo functionality (most of the code is there)
- [ ] Add center crop
- [ ] Add 2 and 3 point modes
- [ ] Add resize on save
- [ ] Add gui controls for loading images, switching modes, and other settings

Also open to pull requests but open issue for discussion first.

- [ ] Add memory limiting
- [ ] General Refactoring
- [ ] Unit Tests / CI
- [ ] GUI in one window ?
- [ ] Installer ?
