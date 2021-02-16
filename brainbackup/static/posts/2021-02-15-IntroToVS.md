---
title: Introduction to Visual Servoing
description: Bridging the gap between manipulation and understanding
tags:
- robotics
- vision processing
---

### Let's Get It Started
Visual servoing (VS) is the practice of using computer vision to control a 
robot's motion. Anytime you pick up or manipulate an object in space, you are
likely using innate VS techniques. As a shameless plug, you can see an example
of visual servoing below:

<a href="/gallery/IntroToVS_1.JPG">
    <img src="/gallery/IntroToVS_1.JPG" alt="Robot Demo" width="350">
</a>

In this scene, we were attempting to use visual features (retro reflective tape)
to guide the robot to pick up field elements from the 2020 FRC game.
 
This quick article is meant to articulate what I have learned on the subject
and show how it can be applied.

### The Weeds

The general visual servoing problem can be summarized as minimizing the
following error:

<img src="https://latex.codecogs.com/svg.latex?\Large&space;e(t)=s(m(t), a) - s^*" title="\Large e(t)=s(m(t), a) - s^*" />

Where:

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;a" title="\Large a" />
is the set of additional information about a system

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;m(t)" title="\Large m(t)" />
is the set of image measurements

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;s(m(t), a)" title="\Large s(m(t), a)" />
is the vector of actual visual features

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;s^*" title="\Large s^*" />
is the vector of desired visual features

The problem as stated may seem trivial. Using the equation above, we
could simply approach this as a controls problem. However as it turns out, 
visual servoing is more focused on solving how we determine 
visual features, or <img src="https://latex.codecogs.com/svg.latex?\Large&space;s" title="\Large s" />
and <img src="https://latex.codecogs.com/svg.latex?\Large&space;s^*" title="\Large s^*" />. 
There are two general approaches to this problem: image-based (IBVS)
and pose-based (PBVS), which we'll subsequently cover over the next two sections.

### Image-based Visual Servoing (IBVS)
As the name suggests, this approach relies on pure visual data. Due
to this, IBVS requires a relation between the pixels in a frame and the motion
of a robot to exist. This relation is going to be known as an 
**interaction matrix**. Using some straight-forward math, we will show how
to derive this matrix for a majority of cases.

First however, it helps to relate the previous parameters to the IBVS approach:

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;a" title="\Large a" />
is a set of parameters related to the camera's specifications
(e.g. focal length)

> <img src="https://latex.codecogs.com/svg.latex?\Large&space;m(t)" title="\Large m(t)" />
is a set of pixel coordinates

#### The Interaction Matrix
<img src="https://latex.codecogs.com/gif.latex?\Large&space;\left\{\begin{matrix}&space;x&space;&&space;=&space;\frac{X}{Z}&space;=&space;\frac{u&space;-&space;c_u}{f\alpha}\\&space;y&space;&&space;=&space;\frac{Y}{Z}&space;=&space;\frac{v&space;-&space;c_v}{f}\\&space;\end{matrix}\right." title="\Large \left\{\begin{matrix} x & = \frac{x}{z} = \frac{u - c_u}{f\alpha}\\ y & = \frac{y}{z} = \frac{v - c_v}{f}\\ \end{matrix}\right." />

> To be updated and continued...
