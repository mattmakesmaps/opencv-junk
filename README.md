# opencv-junk

## General Notes

- Populated `positive` and `negative` image directories with samples.
  - `positive_annotations.txt` created with `opencv_annotation` utility.
  - `negatives.txt` created with bash cmd: `$ for i in negatives/*; do readlink -f $i >> negatives.txt; done;`

- Created binary vector file `postive_vector.vec`: `$ opencv_createsamples -info positive_annotations.txt -vec positive_vector.vec`.

### Model Training

**Initial Run:**

`$ opencv_traincascade -data trained_classifier -vec positive_vector.vec -bg negatives.txt -numPos 44 -numNeg 473 -numStages 20 -precalcValBufSize 2048 -precalcIdxBufSize 2048 2>&1 | tee train_cascade_20stage.log`

This run ended in the following error:

```
===== TRAINING 15-stage =====
<BEGIN
POS count : consumed   44 : 44
NEG count : acceptanceRatio    0 : 0
Required leaf false alarm rate achieved. Branch training terminated.
```

**NOTE:** This isn't an error necessarily, see reference below.

**13 Stage Run:**

This run drops `-nstages`from `20` to `13`, since we got that error in the initial run of 20
`$ opencv_traincascade -data trained_classifier -vec positive_vector.vec -bg negatives.txt -numPos 44 -numNeg 473 -numStages 13 -precalcValBufSize 2048 -precalcIdxBufSize 2048 2>&1 | tee train_cascade_13stage.log`


Going to try adding explicit width and height values.
Need to be same scale as source image (1280x720). Will try 64x36.

`$ opencv_traincascade -data trained_classifier -vec positive_vector.vec -bg negatives.txt -numPos 44 -numNeg 473 -numStages 10 -w 64 -h 36 -precalcValBufSize 2048 -precalcIdxBufSize 2048 2>&1 | tee train_cascade_10stage.log`
## References

- Cascade Classifier Trainer: http://docs.opencv.org/3.2.0/dc/d88/tutorial_traincascade.html
- Coding Robin (Old - See `OUTPUT DURING OPENCV TRAINING`) http://coding-robin.de/2013/07/22/train-your-own-opencv-haar-classifier.html
- Good Explanation "Required leaf false alarm rate achieved." (it's not actually an error) http://answers.opencv.org/question/84852/traincascades-error-required-leaf-false-alarm-rate-achieved-branch-training-terminated/
- http://stackoverflow.com/questions/16058080/how-to-train-cascade-properly
