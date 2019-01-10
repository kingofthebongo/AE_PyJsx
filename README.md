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
# read https://en.wikipedia.org/wiki/Adobe_After_Effects to get correct version number
```

Next use existing functions
```
aeApp.jsOpenScene("PATH/TO/AEPROJECT.aep")
print aeApp.jsGetActiveDocument()
```
Or add yours based on existings

### Prerequisites
After Effects needs to be launched before you can use the functions.
You can run AE from your script thanks to
```
aeApp.openAE()
```
But you have to wait that After Effects is fully loaded before use the other functions.

## Go Further
This script is attempting to compensate the unfilled blank about the After Effects COM & DOM.
Please share your researches if you find the way to handle After Effects with Python like Photoshop.
### Fiew links about After Effects COM & DOM
* **Stackoverflow** [Adobe After Effects COM Object Model ID?](https://stackoverflow.com/questions/50848219/adobe-after-effects-com-object-model-id)
* **Adobe Forum** [Python and After Effects Scripting on Windows](https://forums.adobe.com/thread/2538657)
* **GitHub** [samholt/after-effects-scripting-python](https://github.com/samholt/after-effects-scripting-python)
* **GitHub** [lohriialo/photoshop-scripting-python](https://github.com/lohriialo/photoshop-scripting-python)


## Authors

* **Thibaud CARPENTIER** - *AE Adaptation* - [kingofthebongo](https://github.com/kingofthebongo)

## Reference
Based on **Peter Hanshaw** work for Photoshop: [Use Python to use JavaScript to get Photoshop to do stuff](http://peterhanshawart.blogspot.com/2014/01/use-python-to-use-javascript-to-get.html).
