# Model Creation

Created `positive_annotations_bike_plus_chevron.txt` using:

*NOTE:* cmd interface requires `=`

```bash
opencv_annotation -images=/home/matt/Projects/opencv-sharrow-images/positives/ -annotations-/home/matt/Projects/opencv-sharrow-images/positive_annotations_bike_plus_chevron.txt
```

Ran `average_dimension` utility on above annotation file:

```bash
./average_dimensions -annotations ~/Projects/opencv-sharrow-images/positive_annotations_bike_plus_chevron.txt 
The average dimensions are: w = 338 and h = 136.
```

Notes say recommended input to `create_samples` is under 100px longest dimension. Reduced 4x to w=84 h=34

Create Vector File

*NOTE:* cmd interface for `opencv_createsamples` cannot accept `=`

*NOTE:* when passing `opencv_createsamples` an annotation file that contains **absolute paths**, you must:
    - Execute the `opencv_createsamples` command from the directory in which the annotation file exists.
    - Specify a relative path to the annotation file via the `-info` flag.

**DOES NOT WORK**:

```bash
opencv_createsamples -info /home/matt/Projects/opencv-sharrow-images/positive_annotations_bike_plus_chevron.txt -vec /home/matt/Projects/opencv-junk/run_two/positive_vector_bike_plus_chevron.vec -bg /home/matt/Projects/opencv-sharrow-images/negatives.txt -num 86 -w 84 -h 34
```

**DOES WORK**
```bash
opencv_createsamples -info positive_annotations_bike_plus_chevron.txt -vec /home/matt/Projects/opencv-junk/run_two/positive_vector_bike_plus_chevron.vec -bg /home/matt/Projects/opencv-sharrow-images/negatives.txt -num 86 -w 84 -h 34
```

**OUTPUT**

```bash
matt@matt-XPS-13-9360:~/Projects/opencv-sharrow-images$ opencv_createsamples -info positive_annotations_bike_plus_chevron.txt -vec /home/matt/Projects/opencv-junk/run_two/positive_vector_bike_plus_chevron.vec -bg /home/matt/Projects/opencv-sharrow-images/negatives.txt -num 86 -w 84 -h 34
Info file name: positive_annotations_bike_plus_chevron.txt
Img file name: (NULL)
Vec file name: /home/matt/Projects/opencv-junk/run_two/positive_vector_bike_plus_chevron.vec
BG  file name: /home/matt/Projects/opencv-sharrow-images/negatives.txt
Num: 86
BG color: 0
BG threshold: 80
Invert: FALSE
Max intensity deviation: 40
Max x angle: 1.1
Max y angle: 1.1
Max z angle: 0.5
Show samples: FALSE
Width: 84
Height: 34
Max Scale: -1
Create training samples from images collection...
Done. Created 86 samples
```