# Genetic algorithm for learning an image

This module performs a genetic algorithm for learning an image.
In this particular case, I have chosen an image representing Microsoft's logo. 

### Implementation 

Each individual of the population is represented by an image made up of a fixed number of semi-transparent rectangles.
Each rectangle is defined by two opposite corners and three numbers for RGB values.
Such an image is encoded into a single Gray-coded string.
In such problems, Gray codes can be useful for escaping from local optima.

### Quickstart

```python
pip3 install -r requirements.txt
python3 ImageLearning.py '{"pop_size":10, "pathToImage":"image-learning/Microsoft.jpg", "max_gen":100000}'
```
It is compatible with python 2.7 hence you can easily run it with pip and python
