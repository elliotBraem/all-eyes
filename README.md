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

## Running the tests

TODO: Create tests
TODO: Explain how to run the automated tests for this system

### Break down into end to end tests

TODO: Create tests

## Deployment

TODO: Add additional notes about how to deploy this on a live system

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

### TODO:

- [X] Locate a face in an image
- [X] Locate the eyes on a face
- [ ] Preliminary eye matching
- [ ] Distinguish between closed eyes and open eyes
- [ ] Identify the same set of eyes (open or closed) in the image sequence
- [ ] Apply the replacement to the closed eyes
- [ ] Correct and shadow (In-paint) the replacement to match the image

Misc:
- [ ] auto inject resources/shape_predictor_68_face_landmarks.dat
## Authors

* **Elliot Braem**
* **Connor Waity**
* **Natalie Brooks**
* **Austen Baker**

TODO: See also the list of [contributors](https://github.com/elliotBraem/all-eyes/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Special thanks to Adrian Rosebrock of pyimagesearch
face_detect.py is largly influenced by [his article](https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/)
