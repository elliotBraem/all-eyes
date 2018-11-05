# All-Eyes

  In a photo, closed eyes can occur for a number of reasons, such as the blinding light of a camera’s flash, a mistimed blink, or some other unexpected event. A single individual with closed eyes greatly reduces the picture’s quality and worth, prompting a retake. However, retaking the picture doesn’t ensure that all eyes will be open; a retake is just as much at risk as the initial image. All-eyes attempts to solve this problem using face and closed eye detection, local images, and in-painting to achieve a natural replacement.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

All-eyes is created with Python and OpenCV.

If you do not have Python installed on your machine, please see [Python's Installation Guides](https://docs.python-guide.org/starting/installation/).

If you do not have OpenCV-Python installed on your machine, read ahead to "Installing" or see [OpenCV-Python's Introduction to OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup).
	

## Installing

To setup your environment (specifically for MacOS, let us know if Windows or Linux are different)

1. Create a virtual environment for OpenCV with the name all-eyes (optional, otherwise skip to step 3).

	mkvirtualenv all-eyes -p python3

2. Enter the environment.

	workon all-eyes

3. Install OpenCV (this will have to be done everytime upon entering the session).

	pip install opencv-python

4. Check that OpenCV has been installed by running:

	python3

	import cv2 

	print(cv2.__version__)


Your environment is now setup. Clone this repository with the following command:

	git clone https://github.com/elliotBraem/all-eyes


## Running the tests

TODO: Create tests
TODO: Explain how to run the automated tests for this system

### Break down into end to end tests

TODO: Create tests

## Deployment

TODO: Add additional notes about how to deploy this on a live system

## Contributing

TODO: Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.

### TODO:

- [ ] Locate a face in an image
- [ ] Locate the eyes on a face
- [ ] Preliminary eye matching
- [ ] Distinguish between closed eyes and open eyes
- [ ] Identify the same set of eyes (open or closed) in the image sequence
- [ ] Apply the replacement to the closed eyes
- [ ] Correct and shadow (In-paint) the replacement to match the image

## Authors

* **Elliot Braem**
* **Connor Waity**
* **Natalie Brooks**
* **Austen Baker**

TODO: See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

TODO: 
* Hat tip to anyone whose code was used
* Inspiration
* etc
