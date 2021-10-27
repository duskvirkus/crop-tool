# Crop Tool

A utility for quickly cropping large collections of images.

Inspired by Derrick Schultz's [dataset-tools](https://github.com/dvschultz/dataset-tools).

## Installation

Use installer under releases to install on respective platforms.

## Development

It's suggested that you use Anaconda. Download at: [https://www.anaconda.com/products/individual#Downloads](https://www.anaconda.com/products/individual#Downloads).

```bash
conda create -n crop-tool python=3.6 # python version is important
conda activate
pip install -r requirements.txt
```

Use fbs commands for running building and deployment. See https://github.com/mherrmann/fbs-tutorial for more info on this process.
```bash
fbs run
fbs freeze
fbs installer
```

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
