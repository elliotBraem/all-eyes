# all eyes
#### *A python application able to detect and replace closed eyes in an image*

## Contents
[Motivation](#motivation)

[State of the Art](#state-of-the-art)

[Project Flow](#project-flow)

[Timeline](#timeline)

[Implementation](#implementation)

[Results](#results)

[The Team](#the-team)

[The Process](#the-process)

[The Solution](#the-solution)

[Plans for Improvement](#plans-for-improvement)


## Motivation
In a photo, closed eyes can occur for a number of reasons, such as the blinding light of a camera’s flash, a mistimed blink, or some other unexpected event. A single individual with closed eyes greatly reduces the picture’s quality, usually prompting a retake. However, retaking the picture does not ensure that all eyes will be open; a retake is just as prone to mistakes as the initial image. All-eyes attempts to solve this problem using face and closed eye detection, local images, and in-painting to achieve a natural, low cost replacement.

Especially juxtaposed with other state of the art options, our solution is quick and easy, and does not require a huge bank of photos or complicated and time consuming AI functionality. We would call it the 'perfect balance' between cost and effectiveness.


## State of the Art
#### **Facebook’s Eye In-Painting with Exemplar Generative Adversarial Networks**

Facebook’s Eye In-Painting technique utilizes in-painting as a backbone for a sophisticated system of machine learning that occurs through the interaction of two processes. In-painting is a process that synthesizes patches for holes in an image using the pixels around it. It can be used to help smooth out an image and make the different components of it consistent with one another. Facebook’s version of in-painting is an algorithm that breaks down the image into structural and textural components, which are then used to aid in constructing patches for holes that will be consistent with the rest of the image (in terms of lighting, color, contrast, etc.). Facebook replaces the closed eyes with open eyes from another image of the same person, then uses two processes to perform the in-painting. One process constructs the patches while another process checks how realistic the patches are by referencing a bank of pictures.

See references: [Facebook Eye In-Painting Paper](https://research.fb.com/wp-content/uploads/2018/06/Eye-In-Painting-with-Exemplar-Generative-Adversarial-Networks.pdf) and [Forbes Article on Facebook Eye In-Painting](https://www.forbes.com/sites/paulmonckton/2018/06/21/how-facebook-can-open-your-eyes/#65235a5a6d16).

#### **Adobe Photoshop’s “Open Closed Eyes” Feature**

Photoshop’s “Open Closed Eyes” element is a procedure that requires quite a few steps and is essentially a direct cut-and-paste method with in-painting. The user identifies a closed eye, then chooses a .png image (in this case, a cutout of eyes) to copy from where a person’s eyes are open. The open eyes then replace the closed eyes and Photoshop performs its own in-painting to make the result appear realistic. This method is relatively inflexible, in the sense that eyes taken from a picture that were not in the same lighting or from exactly the same angle may not look realistic or consistent with the structure/texture of the rest of the image after in-painting.

See references: [Essential Photoshop Elements: Open Closed Eyes Tutorial](https://www.essential-photoshop-elements.com/open-closed-eyes-with-Photoshop-Elements-2018.html) and [Digital Photography for Moms: Open Closed Eyes Tutorial](https://www.digitalphotographyformoms.com/open-closed-eyes-in-photoshop-elements-quick-tip/).

#### **Google’s “Image Cache for Replacing Portions of Images”**

Google’s approach is much like that of Photoshop’s, in that it uses a cut-and-paste method, where the closed eyes are overlaid with clipped open eyes taken from another picture. However; since Google’s method builds its image database automatically from all a person’s pictures, the database is much more comprehensive and can be searched through much more efficiently for an optimal clipping. Of course, the best optimization of this method relies on a person’s image database to be considerably large in order for there to be enough options, and at worst, it has the same results as Photoshop, but is faster and less complicated to use.

See references: [What a Future: Google Photos New Feature](http://www.whatafuture.com/google-photos-new-feature/) and [US Patent and Trademark Office: "Image Cache for Replacing Portions of Images](http://appft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.html&r=16&p=1&f=G&l=50&d=PG01&S1=(20170413.PD.+AND+(Google.AS.+OR+Google.AANM.))&OS=PD/04/13/2017+AND+(AN/Google+OR+AANM/Google)&RS=(PD/20170413+AND+(AN/Google+OR+AANM/Google))).


## Project Flow
![Project Flow Diagram](diagram.jpeg)


## Timeline

| Task | Target Date |
| :--- | ---: |
| Locate a face in an image | X |
| Locate the eyes on a face | X |
| Preliminary eye matching | X |
| Distinguish between closed and opened eyes | November 5th |
| Identify the same set of eyes in the image sequence | November 15th |
| Apply the replacement to the closed eyes | November 20th |
| In-Paint the replacement to match the image | November 30th |

## Implementation
Code may be accessed on Github at [All-Eyes](https://github.com/elliotBraem/all-eyes).


## Results
Link to project presentation slides [here](https://docs.google.com/presentation/d/1sczYU9fbb02LyJrjiifcD8XKOPWxBFJg4SAKT955yOE/edit?usp=sharing).

## The Team
#### **Elliot Braem**  
![Elliot Looking Horrific](img/team/elliot.jpg)  
*Computer Science major, graduating 2019*  
email: braemelliot@gmail.com  

#### **Connor Waity**  
![Connor Looking Horrific](img/team/connor.jpg)  
*Computer Science major, graduating UP YOUR BUTT*  
email: cbwaity@wisc.edu  

#### **Natalie Brooks**  
![Natalie Looking Horrific](img/team/natalie.jpg)  
*Computer Science major, graduating 2019*  
email: natalierose7465@gmail.com  

#### **Austen Baker**  
![Austin Not Looking Horrific](img/team/austin.jpg)  
*Computer Science major, graduating 2020*  
email: austenbaker225@gmail.com  


## The Process
#### **Initial Face Detection**

![Faces Detected](img/process/initial_detection.jpg)

In order to get a feel for the project, we first implemented a preliminary face detection using Haar Cascade, as provided by Python OpenCV. Haar Cascade is based on the Viola-Jones Object Detection Algorithm, which is trained a large set of positives and negatives, then uses certain features to determine if an object is detected. The detectMuliScale parameter must be tuned in order to detect all objects in an image, but does not always work from image-to-image.

![Simple Features](img/process/features.jpg)

In most cases, Haar Cascade was able to detect all of the faces in a given image, however, false positives were also common. Moreover, because eyes are more abstract and less clear than faces, the Haar Cascade failed to detect them most of the time.

See tutorial for Haar Cascade as provided by Python OpenCV [here](https://docs.opencv.org/3.4/d7/d8b/tutorial_py_face_detection.html).


#### **Superior Facial Detection with dlib**

![dlib Facial Detection](img/process/dlib_detection.jpg)

In order to improve accuracy, we converted to a HOG-Based face detection which proved to be more robust in detecting faces and had less false-positives. Once the face is detected, we use a predictor to identify facial features. It identifies facial features relative to their position on the face and is much more reliable since, for every face detected, two eyes are always detected as well.

![dlib Facial Landmarks](img/process/feature_points.jpg)

See tutorial for dlib's facial landmark detector [here](https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/).

#### **Open/Closed Eye Detection**

![Open/Closed Eye Detection](img/process/open_eye_detect.jpg)

Given dlib's six point eye area, we are able to determine whether an eye is open or not based on the ratio of the top of the eye to the bottom. Given formula and re ....... ????

![Eye Point Formula](img/process/formula.jpg)

TBC

![6 Critical Eye Points](img/process/close_eye_detect.jpg)



## The Solution

TODO


## Plans for Improvement
There is a lot to be done along the lines of editing photos based on a photo bank. Specifically with group pictures, it is not uncommon for a member of the group to not be smiling, which could be selected from the photo bank, superimposed onto the photo, then in-painted to look realistic, much like we have accomplished regarding eyes with our project.

Of course, there are always improvements to be made in trying to get the most cost effective *realistic* results, which relies a lot on the intricacies of in-painting. A worth while improvement to pursue would be a general and time-efficient fix to the uncanny results of some of the superimposed eyes.
