# random-forest-for-exoplanets
# random-forest-exoplanets

## About
This is a implementation of a random forest from scratch in Python designed to classify star lightcurves in order to detect exoplanets. This was done as a method of trying to get a better idea of what was going on inside random forest models when I ran them from higher-level ML libraries, and was an exercise in trying to use better Python programming techniques and proper OOP.

Alternatively, this doubles as an overly complex coin flipping simulator as its accuracy is always ~50%. 

I keep telling myself I'm going to revisit this and give it a good fixing up but I remain uncompelled to do so and as a result it will remain in its current form.

## Usage
If for some reason you would like to see this model in action, clone the repository then call randomforest.py with the proper arguments.
```
git clone https://github.com/richardfeynmanrocks/random-forest-exoplanets.git
python randomforest.py PATH_TO_INPUT_CSV NUM_TREES DEPTH
```
