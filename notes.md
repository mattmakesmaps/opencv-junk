# Model Creation

## Prepare Training Data

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
matt@matt-XPS-13-9360:~/Projects/opencv-sharrow-images$ opencv_createsamples -info positive_annotations_bike_plus_chevron.txt -vec /home/matt/Projects/opencv-junk/classifier/run_two/positive_vector_bike_plus_chevron.vec -bg /home/matt/Projects/opencv-sharrow-images/negatives.txt -num 86 -w 84 -h 34
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

## Train the Model

### LBP

```bash
opencv_traincascade -data /home/matt/Projects/opencv-junk/classifier/run_two/cascade_xmls -numPos 73 -numNeg 172 -vec /home/matt/Projects/opencv-junk/classifier/run_two/positive_vector_bike_plus_chevron.vec -bg /home/matt/Projects/opencv-sharrow-images/negatives.txt -w 84 -h 34 -precalcValBufSize 2048 -precalcIdxBufSize 2048 -featureType LBP
```

Where:

`-numPos` == 0.85 * 86 positive samples
`-numNeg` == 2 * 86 = 172 (e.g. double number of positive samples)
`-featurType == LBP (integer calcs vs floating calcs... faster, less precise)
`-w` and `-h` == 24 because we need to specify something... using the defaults. NOTE: Should this be a ratio of, or exact match to, our vector inputs (-w=84 -h=34)
**UPDATE**: `opencv_traincascade` kept failing until i set `-w` and `-h` to reflect inputs for `opencv_createsamples`

Final Stage Output:

```
===== TRAINING 19-stage =====
<BEGIN
POS count : consumed   73 : 73
NEG count : acceptanceRatio    172 : 0.000723495
Precalculation time: 0
+----+---------+---------+
|  N |    HR   |    FA   |
+----+---------+---------+
|   1|        1|        1|
+----+---------+---------+
|   2|        1| 0.151163|
+----+---------+---------+
END>
```

Observations:
- Final `acceptanceRatio` value did not hit 0.00001
- Number of distinct features at stage 19 is 2, should be higher according to docs, lore...

### HAAR

```bash
opencv_traincascade -data /home/matt/Projects/opencv-junk/classifier/run_two/cascade_xmls -numPos 73 -numNeg 172 -vec /home/matt/Projects/opencv-junk/classifier/run_two/positive_vector_bike_plus_chevron.vec -bg /home/matt/Projects/opencv-sharrow-images/negatives.txt -w 84 -h 34 -precalcValBufSize 2048 -precalcIdxBufSize 2048 -featureType HAAR
```

Final Stage Output:

```
===== TRAINING 19-stage =====
<BEGIN
POS count : consumed   73 : 73
NEG count : acceptanceRatio    172 : 1.83403e-05
Precalculation time: 21
+----+---------+---------+
|  N |    HR   |    FA   |
+----+---------+---------+
|   1|        1|        1|
+----+---------+---------+
|   2|        1|        1|
+----+---------+---------+
|   3|        1|        1|
+----+---------+---------+
|   4|        1| 0.575581|
+----+---------+---------+
|   5|        1| 0.616279|
+----+---------+---------+
|   6|        1| 0.354651|
+----+---------+---------+
END>
Training until now has taken 0 days 0 hours 56 minutes 39 seconds.
```