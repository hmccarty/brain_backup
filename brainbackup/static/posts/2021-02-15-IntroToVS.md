---
title: Introduction to Visual Servoing
description: Bridging the gap between manipulation and understanding
tags:
- robotics
- vision processing
---

### Getting Started
Visual servoing (VS) is the practice of using computer vision to control a 
robot's motion. Anytime you pick up or manipulate an object in space, you are
likely using innate VS techniques. As a shameless plug, you can see an example
of visual servoing below:

<a href="/gallery/IntroToVS_1.JPG">
    <img src="/gallery/IntroToVS_1.JPG" alt="Robot Demo" width="450">
</a>

In this scene, we were attempting to use visual features (retro reflective tape)
to guide the robot to pick up field elements from the 2019 FRC game.
 
This article is meant to gently introduce the principle ideas of visual
servoing.

### Basic Idea
There are three main components to visual servoing:

1. Understanding your environment visually

2. Choosing the desired state of your environment

3. Using control methodolgies to reach your desired state

These main components can be summarized to minimizing the following error:

<img src="https://latex.codecogs.com/svg.latex?\Large&space;e(t)=s(m(t), a) - s^*" title="\Large e(t)=s(m(t), a) - s^*" />

Where:

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;m(t)" title="\Large m(t)" />
is the set of image measurements

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;a" title="\Large a" />
is a set of additional information about a system

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;s(m(t), a)" title="\Large s(m(t), a)" />
is the vector of actual features

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;s^*" title="\Large s^*" />
is the vector of desired features

Different visual servoing schemes arise in where error is being minimized.
In this article, we'll cover the two generally seen methods: image-based VS 
(IBVS) and pose-based VS (PBVS).

### Image-based Visual Servoing (IBVS)
Image-based visual servoing reduces error directly within the image space.

What does this mean? 
Essentially, our prime goal is to make our current image look like
a desired image:

<a href="/gallery/IntroToVS_2.JPG">
    <img src="/gallery/IntroToVS_2.JPG" alt="IBVS Basic" width="450">
</a>

This probably prompts an obvious question: how do we control our robot to reduce
that error?

This is where the interaction matrix comes into play.

The interaction matrix (<img src="https://latex.codecogs.com/gif.latex?\Large&space; L" title="L" />) defines:

<img src="https://latex.codecogs.com/gif.latex?\Large&space;e=Lv" title="\Large e=Lv" />

Which allows you to relate the movement of your vehicle to image-based error.

I'm going to spare the math to derive <img src="https://latex.codecogs.com/gif.latex?\Large&space; L" title="L" /> as this is meant to be a simple introduction, however you can find a lot more information in [1].

### Pose-based Visual Servoing (PBVS)
Pose-based visual servoing reduces error within the cartesian space.

This means we can use typical control techniques to move towards our desired
state, but we also need to convert objects within our image to 3D space.

Again this requires an interaction matrix, which projects visual features into
3D points in cartesian space.

### Conclusion
As previously stated, this only meant to be an introduction to visual servoing.
If you are interested in learning more, I recommend the sources below.

Good luck!

### Sources
[1] https://link.springer.com/chapter/10.1007/978-3-319-32552-1_34#Sec2

[2] https://control.com/technical-articles/an-overview-of-visual-servoing-for-robot-manipulators/
