# AE_PyJsx

Python to JSX bridge for Adobe After Effects.

## Usage

Initialize the AE wrapper
```
aeApp = AE_JSInterface()
```
Or, use specific parameters.
```
aeApp = AE_JSInterface(aeVersion, returnFolder)
```

Next use existings functions
```
aeApp.jsOpenScene("PATH/TO/AEPROJECT.aep")
print aeApp.jsGetActiveDocument()
```

Or add yours based on existings

## Authors

* **Thibaud CARPENTIER** - *AE Adaptation* - [kingofthebongo](https://github.com/kingofthebongo)

Based on Peter Hanshaw work for Photoshop: [Use Python to use JavaScript to get Photoshop to do stuff](http://peterhanshawart.blogspot.com/2014/01/use-python-to-use-javascript-to-get.html).
