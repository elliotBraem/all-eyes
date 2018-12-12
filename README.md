# All-Eyes

  In a photo, closed eyes can occur for a number of reasons, such as the blinding light of a camera’s flash, a mistimed blink, or some other unexpected event. A single individual with closed eyes greatly reduces the picture’s quality and worth, prompting a retake. However, retaking the picture doesn’t ensure that all eyes will be open; a retake is just as much at risk as the initial image. All-eyes attempts to solve this problem using face and closed eye detection, local images, and in-painting to achieve a natural replacement.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

All-eyes is created with Python and [OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup).
If you do not have Python installed on your machine, please see [Python's Installation Guides](https://docs.python-guide.org/starting/installation/).
	

## Installing

1. Clone this repository with the following command:
```
	git clone https://github.com/elliotBraem/all-eyes
```
	
2. Optional: Create a virtual environment for OpenCV with the name all-eyes and enter the environment.
```
	mkvirtualenv all-eyes -p python3
	workon all-eyes
```

3. Run setup.py to install the project and dependencies:
```
	python setup.py install
```

## Usage

After installing the project:

1. Place multiple retakes of the same group picture in the directory (or provide custom path in next step):
```
	all-eyes/resources/images
```

2. Run the following command:
```
	python all_eyes [-b base image] [-i image directory]
```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

### TODO:

- [X] Locate a face in an image
- [X] Locate the eyes on a face
- [X] Preliminary eye matching
- [X] Preliminary open/closed implementation
- [X] Distinguish between closed eyes and open eyes
- [X] Identify the same set of eyes (open or closed) in the image sequence
- [X] Apply the replacement to the closed eyes
- [X] Inpaint the replacment eye
- [ ] Improved, natural inpainting

Misc:
- [ ] auto inject resources/shape_predictor_68_face_landmarks.dat
## Authors

* **Elliot Braem**
* **Connor Waity**
* **Natalie Brooks**
* **Austen Baker**

See also the list of [contributors](https://github.com/elliotBraem/all-eyes/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Special thanks to Adrian Rosebrock of pyimagesearch. Aspects of this project are largly influenced by his articles:
* **[Facial landmarks with dlib, OpenCV, and Python](https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/)**
* **[Detect eyes, nose, lips, and jaw with dlib, OpenCV, and Python](https://www.pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/)**
