# Parallelized-Facial-Recognition
A facial recognition system that is parallelized in order to speed up the computational performance.

#### Keyword: Facial Recognition, Biometrics, Computer Vision, Image Processing, Parallelization, PyQt5


Table of contents
=================
- [I.Introduction](#iintroduction)
- [II.Description](#iidescription)
- [III.Used dependency configuration](#iiiused-dependency-configuration)
- [VI.Implementation](#viimplementation)
- [VII.Results](#viiresults)
- [VIII.Concusion](#viiiconcusion)


I.Introduction
==============
* This is my assignment in the course "Embedded System Programming" at my university.
* In this project, I try to implement a facial recognition into an embedded computer, e.g., Raspberry Pi 3. In which, I did not write the facial recognition algorithm. However, I just implement available functions on the Raspberry. The facial algorithm is derived from this [Github repository](https://github.com/ageitgey/face_recognition).
* **My contributions** are **parallelizing** the available algorithm and making a easily **interactive GUI**. Python 3 is the used language and the implementation is runned in Ubuntu 16.04.


II.Description
==============
* According to the author of the [repository](https://github.com/ageitgey/face_recognition), the algorithm includes three phases, namely Face detection, Face normalization, and Face recognition. You can explore more about how such phases run in [this Medium link](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78).
* The picture below depicts the CPU utilization when running the algorithm. As can be seen, the algorithm is written for single core configuration, meanwhile, the Raspberry can have 4 CPU threads to process. This lead to a bad utilization. Therefore, I want to improve this shortcoming so that the hardware-limited Raspberry can run the complex algorithm.

<p align="center">
  <img src="https://github.com/AntiAegis/Paralledized-Facial-Recognition/blob/master/single-core.png" width="600" alt="accessibility text">
</p>

* To deal with this limitation, I propose a system architecture as the following picture. Here, with four CPU threads, each thread is reposible for a specific task. Concretely, when a frame of video comes, the thread 1 receives it, display it into the screen, and send it to the thread 2. Thread 2 is to detect face by pointing out coordinates of vertices of the bounding boxes of faces in the image. Then, thread 3 uses the output of thread 2 to crop image to bounding boxes of faces and encode them as face embeddings. Finally, the last thread takes extracted face embeddings so as to perform a matching with templates saved in the database.

<p align="center">
  <img src="https://github.com/AntiAegis/Paralledized-Facial-Recognition/blob/master/multi-core.png" width="600" alt="accessibility text">
</p>


III.Used dependency configuration
=================================
* Ubuntu 16.04
* Python 3.5
* OpenCV 3.3.1
* [face_recognition](https://pypi.org/project/face_recognition/)
* PyQt5


VI.Implementation
=================
* There are three folders, e.g., "1.original-system", "2.parallelized-system", and "3.GUI-integrated-system". In which, they contain original-system code, parallelized-system code, and a GUI-integrated code, respectively.

* To parallelize the original system in Python 3, I use [Process-based “threading” interface](https://docs.python.org/2/library/multiprocessing.html).

* Note that the GUI-integrated code in the folder "3.GUI-integrated-system" is just used in PC. I have not developed any version to run GUI on the Raspberry.


VII.Results
============
* The table below shows the comparation between two system (parallelized and original). Clearly, the parallelized system has the CPU utilization better than the original one.

<p align="center">
  <img src="https://github.com/AntiAegis/Paralledized-Facial-Recognition/blob/master/compare.png" width="700" alt="accessibility text">
</p>


VIII.Concusion
==============
* The advantages and disadvantages of my proposal are listed in the following table.

<p align="center">
  <img src="https://github.com/AntiAegis/Paralledized-Facial-Recognition/blob/master/pros-and-cons.png" width="700" alt="accessibility text">
</p>
