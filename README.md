<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
    <h1> Object Tracking Open Cv</h1>
  <p align="center">
    A set of projects to learn about Computer Vision
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#car-counter">Car Counter</a>
      <ul>
        ![Result](https://github.com/LukaFlores/object-tracking-opencv/assets/85141937/a6d8c7fd-ba35-4f63-bb3c-29cc9249967f)
      </ul>
    </li>
  </ol>
</details>


<!-- GETTING STARTED -->
## Getting Started

This is a python project

### Prerequisites

1. Install all the requirements

```
pip install -r requirements.txt
```

### Installation

 step by step series of examples that tell you how to get a development env running

1. Install all the requirements

```
git clone https://github.com/LukaFlores/object-tracking-opencv.git
```

2. Change into specific Project Directory (e.g /Car-Counter)
```
cd Car-Counter
```

3. Run the Program
```
./build.sh
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Car Counter -->
## Car Counter

Inspired by [youtube project](https://www.youtube.com/watch?v=WgPbbWmnXJ8&t=75s) in which goal of the car counter is to track the number of cars that pass north and south on the freeway

#### How it was done

1. A mask was overlaid on the video to the area in which the vehicles could be identified. A bitwise * and * function was used to find the shared space of the mask and the video frame [Code](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L52C1-L53)

<div align="center">
    <img src="Car-Counter/Video/readme-mask.png" alt="Logo" width="500" />
</div>

2. The current frame (with the mask) is then assessed by the [Yolo Model](https://docs.ultralytics.com), which tries to identify one of the labels in this [list](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L13C1-L30C2), after detection it will produce a [list](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L55) 
of boxes bounding the object. We are left with the image recognition of vehicles after [filtering](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L81-L84) for objects and confidence.

3. [Abewley's realtime tracking algorithm](https://github.com/abewley/sort) assesses the age in which the object is not seen throughout frames ([max_age](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L36)), the is the minimum value of hit streak to continue tracking ([min_hits](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L36)) and the common characteristics of a specific object across frames ([iou_threshold](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L36))
Which as a results tracks a specific object across multiple frames.

4. Finally to keep counter an [origin](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L114-L116) is placed at the center of each object, once it crosses the respective [line](https://github.com/LukaFlores/object-tracking-opencv/blob/05fad2bb24db0296b3b97c996344c7752614ea34/Car-Counter/main.py#L99-L100) it is added to the overall tally.

## Result

![Result](https://github.com/LukaFlores/object-tracking-opencv/assets/85141937/a6d8c7fd-ba35-4f63-bb3c-29cc9249967f)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



